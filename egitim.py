from ultralytics import YOLO

# 1. YOLOv11 nano modelini yükle (En hızlı ve hafif modeldir)
model = YOLO('yolo11n.pt')

# 2. Eğitimi başlat
if __name__ == '__main__':
    model.train(
        data='Altay Kare Tanimlama.v3i.yolov11\data.yaml', # İndirdiğin klasörün adını tam buraya yaz
        epochs=100,                     # 100 tur eğitim başlangıç için idealdir
        imgsz=640,                      # Roboflow'da belirlediğimiz görsel boyutu
        device='cpu',                       # NVIDIA ekran kartın varsa 0 kalsın, yoksa 'cpu' yaz
        workers=2  ,                     # Bilgisayarı çok yormaması için 2 iyidir
        name = 'kare_model_v3'
    )