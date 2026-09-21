from ultralytics import YOLO
import cv2

# 1. Eğittiğin en iyi modeli yükle
# Not: 'train' klasörünün numarasını (train, train2 vb.) kontrol et
model = YOLO('runs/detect/kare_model_v3/weights/best.pt')

# 2. Test etmek istediğin fotoğrafın veya videonun yolunu yaz
# Örnek: 'deneme.jpg' veya 'test_video.mp4'
kaynak = 'deneme videosu.mp4'

# 3. Tahmini gerçekleştir
results = model.predict(source=kaynak, save=True, conf=0.8)

print("--- TEST TAMAMLANDI ---")
print("Sonuçlar 'runs/detect/predict' klasörüne kaydedildi.")