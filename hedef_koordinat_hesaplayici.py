"""
SGM ASENA - Hedef Jeolokasyon ve Koordinat Dönüşüm Modülü
---------------------------------------------------------
Bu modül, İHA üzerindeki kameradan tespit edilen piksel koordinatlarını (u, v),
Pixhawk otopilotundan alınan telemetri verileri (İrtifa, Enlem, Boylam, Pitch, Roll, Yaw)
ve kamera optik parametreleri ile birleştirerek hedefin Dünya üzerindeki gerçek
WGS84 GPS (Enlem, Boylam) koordinatlarını hesaplar.

Yazar: SGM ASENA Ekibi
Lisans: MIT
"""

import math
from typing import Tuple, Dict, Any

class GeoTargetCalculator:
    def __init__(self, 
                 image_width: int = 1920, 
                 image_height: int = 1080, 
                 hfov_deg: float = 82.0, 
                 vfov_deg: float = 52.0):
        """
        Kamera ve görüntü düzlemi parametrelerini başlatır.
        
        :param image_width: Kamera görüntü genişliği (piksel)
        :param image_height: Kamera görüntü yüksekliği (piksel)
        :param hfov_deg: Kameranın yatay görüş açısı (derece)
        :param vfov_deg: Kameranın dikey görüş açısı (derece)
        """
        self.img_w = image_width
        self.img_h = image_height
        self.hfov_rad = math.radians(hfov_deg)
        self.vfov_rad = math.radians(vfov_deg)
        
        # Kamera merkez pikselleri (Principal Point)
        self.cx = self.img_w / 2.0
        self.cy = self.img_h / 2.0

        # Dünya yarıçapı (WGS84 ortalama metre)
        self.EARTH_RADIUS = 6378137.0

    def pixel_to_ground_offset(self, 
                               u: float, 
                               v: float, 
                               altitude_m: float, 
                               pitch_deg: float = 0.0, 
                               roll_deg: float = 0.0) -> Tuple[float, float]:
        """
        Görüntü üzerindeki piksel merkezini (u, v), İHA gövde eksenindeki
        metre cinsinden yer sapmasına (dx: sağ/doğu, dy: ileri/kuzey) dönüştürür.
        
        :param u: Hedef merkezinin yatay piksel konumu (0 <= u <= img_w)
        :param v: Hedef merkezinin dikey piksel konumu (0 <= v <= img_h)
        :param altitude_m: İHA'nın yerden yüksekliği (AGL - Above Ground Level)
        :param pitch_deg: İHA'nın yunuslama açısı (burun yukarı pozitif)
        :param roll_deg: İHA'nın yatış açısı (sağa yatış pozitif)
        :return: (dx_body, dy_body) metre cinsinden gövde eksenindeki sapma
        """
        # Merkezden piksel sapması
        dx_px = u - self.cx
        dy_px = self.cy - v  # Görüntüde yukarı yön pozitif dy

        # Pinhole kamera projeksiyonu açısı
        alpha_x = (dx_px / self.cx) * (self.hfov_rad / 2.0)
        alpha_y = (dy_px / self.cy) * (self.vfov_rad / 2.0)

        # İHA yönelim açılarını ekle
        total_angle_x = alpha_x + math.radians(roll_deg)
        total_angle_y = alpha_y + math.radians(pitch_deg)

        # Metre cinsinden yer izdüşümü
        dx_body = altitude_m * math.tan(total_angle_x)
        dy_body = altitude_m * math.tan(total_angle_y)

        return dx_body, dy_body

    def calculate_target_gps(self, 
                             u: float, 
                             v: float, 
                             uav_lat: float, 
                             uav_lon: float, 
                             altitude_m: float, 
                             yaw_deg: float, 
                             pitch_deg: float = 0.0, 
                             roll_deg: float = 0.0) -> Dict[str, Any]:
        """
        Hedef pikselinden mutlak WGS84 GPS koordinatını hesaplar.
        
        :param u: Hedef X pikseli
        :param v: Hedef Y pikseli
        :param uav_lat: İHA'nın enlemi (derece)
        :param uav_lon: İHA'nın boylamı (derece)
        :param altitude_m: İHA'nın irtifası (AGL, Lidar veya Barometre)
        :param yaw_deg: İHA'nın baş açısı (Kuzey = 0°, Doğu = 90°)
        :return: Sözlük formatında hedef enlem, boylam ve sapma mesafesi
        """
        dx_body, dy_body = self.pixel_to_ground_offset(u, v, altitude_m, pitch_deg, roll_deg)
        
        # Gövde koordinatlarını (Body Frame) Dünya Kuzey-Doğu eksenine (NED) döndür
        yaw_rad = math.radians(yaw_deg)
        
        # İleri eksen (North) ve Yan eksen (East) dönüşümü
        d_north = dy_body * math.cos(yaw_rad) - dx_body * math.sin(yaw_rad)
        d_east  = dy_body * math.sin(yaw_rad) + dx_body * math.cos(yaw_rad)

        # Metre sapmasını dereceye çevir (WGS84 düzlemsel yaklaşım)
        d_lat = (d_north / self.EARTH_RADIUS) * (180.0 / math.pi)
        d_lon = (d_east / (self.EARTH_RADIUS * math.cos(math.radians(uav_lat)))) * (180.0 / math.pi)

        target_lat = uav_lat + d_lat
        target_lon = uav_lon + d_lon
        horizontal_distance = math.sqrt(d_north**2 + d_east**2)

        return {
            "target_lat": target_lat,
            "target_lon": target_lon,
            "d_north_m": d_north,
            "d_east_m": d_east,
            "ground_distance_m": horizontal_distance,
            "uav_altitude_m": altitude_m
        }

if __name__ == "__main__":
    # Örnek Doğrulama Testi
    calculator = GeoTargetCalculator(image_width=1920, image_height=1080, hfov_deg=82.0, vfov_deg=52.0)
    
    # İHA: Konya Teknik Üniversitesi Üzerinde, 50 metre irtifada, 45 derece baş açısında
    uav_lat = 37.9838
    uav_lon = 32.5593
    altitude = 50.0 # metre
    yaw = 45.0      # derece
    
    # Hedef kameranın hafif sağ-altında tespit edilmiş olsun
    target_u = 1200
    target_v = 700
    
    sonuc = calculator.calculate_target_gps(
        u=target_u, 
        v=target_v, 
        uav_lat=uav_lat, 
        uav_lon=uav_lon, 
        altitude_m=altitude, 
        yaw_deg=yaw
    )
    
    print("\n--- SGM ASENA HEDEF JEOLOKASYON DOĞRULAMA TESTİ ---")
    print(f"İHA Mevcut Konum     : Lat: {uav_lat:.6f}, Lon: {uav_lon:.6f}, İrtifa: {altitude}m")
    print(f"Hedef Piksel (u, v)  : ({target_u}, {target_v})")
    print(f"Hesaplanan Hedef GPS : Lat: {sonuc['target_lat']:.6f}, Lon: {sonuc['target_lon']:.6f}")
    print(f"Hedefe Yatay Mesafe  : {sonuc['ground_distance_m']:.2f} metre")
    print(f"Kuzey / Doğu Sapması : dN = {sonuc['d_north_m']:.2f}m, dE = {sonuc['d_east_m']:.2f}m")
