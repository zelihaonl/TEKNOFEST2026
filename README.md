# SGM ASENA - İHA Destekli Otonom Hedef Tespit ve Konumlandırma Sistemi

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![YOLO11](https://img.shields.io/badge/YOLO-v11-00FFFF.svg)](https://github.com/ultralytics/ultralytics)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Proje Hakkında

**SGM ASENA**, İnsansız Hava Araçları (İHA) vasıtasıyla havadan görüntü alarak hedef tespiti yapan ve tespit edilen hedeflerin coğrafi konumunu (WGS84 GPS) gerçek zamanlı olarak hesaplayan yapay zekâ tabanlı bir hedef tespit ve takip sistemidir.

Proje, afet durumları, arama-kurtarma operasyonları ve taktik saha senaryolarında, havadan tespit edilen kritik hedeflerin konumlarını anında belirleyerek müdahale birimlerine veya sahadaki otonom araçlara aktarmayı amaçlamaktadır.

---

## ✨ Temel Özellikler

- **Gerçek Zamanlı Hedef Tespiti:** Güncel **YOLO11** mimarisi kullanılarak hava görüntülerinde yüksek doğruluk ve hızla nesne tespiti.
- **Hedef Jeolokasyon (GPS Hesaplama):** İHA telemetri verileri (irtifa, açı, anlık GPS konumu) ve kamera parametreleri harmanlanarak hedefin yeryüzündeki kesin koordinatlarının (Enlem, Boylam) hesaplanması.
- **Kenar Bilişim Optimizasyonu:** NVIDIA Jetson ve gömülü sistemler üzerinde yüksek FPS elde edebilmek için ONNX ve OpenVINO/TensorRT formatlarına model dönüştürme altyapısı.
- **Modüler ve Esnek Yapı:** Eğitim, test, optimizasyon, koordinat kestirimi ve canlı çıkarım işlevlerinin bağımsız modüller olarak çalıştırılabilmesi.

---

## 📁 Proje Dosya Yapısı

| Dosya | Açıklama |
| :--- | :--- |
| `canli_tahmin.py` | Video veya kamera akışında canlı nesne tespiti ve görselleştirme |
| `hedef_koordinat_hesaplayici.py` | Piksel sapmalarından WGS84 GPS koordinatı hesaplayan matematiksel modül |
| `egitim.py` | YOLO11 modelinin özel veri seti ile eğitimi |
| `test_et.py` | Eğitilmiş modelin başarım metriklerinin test edilmesi |
| `optimize.py` | Modelin ONNX / OpenVINO formatlarına dönüştürülmesi |
| `benchmark.py` | Çıkarım hızı ve gecikme (latency/FPS) testleri |
| `veri_indir.py` | Roboflow üzerinden veri seti indirme yardımcısı |

---

## 🚀 Hızlı Başlangıç

### 1. Kurulum
```bash
# Depoyu klonlayın
git clone https://github.com/kullanici_adiniz/IHA_YOLOv11.git
cd IHA_YOLOv11

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### 2. Canlı Tahmin Testi
Eğitilmiş model ile video akışı üzerinde tespit çalıştırmak için:
```bash
python canli_tahmin.py
```

### 3. Hedef Koordinat Kestirimi Testi
İHA telemetri verileriyle hedef koordinatının hesaplanmasını simüle etmek için:
```bash
python hedef_koordinat_hesaplayici.py
```

---

## 👥 Takım

**SGM ASENA Takımı - Konya Teknik Üniversitesi**  
Yapay Zekâ, Aviyonik ve Otonom Sistemler Çalışma Grubu

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) kapsamında lisanslanmıştır.
