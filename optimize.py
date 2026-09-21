from ultralytics import YOLO
import os

def export_models():
    # En iyi model ağırlık dosyasının yolu
    model_path = 'runs/detect/kare_model_v3/weights/best.pt'
    
    if not os.path.exists(model_path):
        print(f"Hata: En iyi model ağırlık dosyası bulunamadı! Yol: {model_path}")
        print("Lütfen 'runs/detect/kare_model_v3/weights/best.pt' dosyasının varlığından emin olun.")
        return

    print(f"Model yükleniyor: {model_path}")
    model = YOLO(model_path)

    # 1. ONNX formatına dönüştür
    print("\n--- ONNX Dönüşümü Başlatılıyor ---")
    try:
        onnx_path = model.export(format='onnx', simplify=True)
        print(f"Başarılı: ONNX formatında kaydedildi. Dosya: {onnx_path}")
    except Exception as e:
        print(f"Hata: ONNX dışa aktarma başarısız oldu: {e}")

    # 2. OpenVINO formatına dönüştür
    print("\n--- OpenVINO Dönüşümü Başlatılıyor ---")
    try:
        openvino_path = model.export(format='openvino')
        print(f"Başarılı: OpenVINO formatında kaydedildi. Klasör: {openvino_path}")
    except Exception as e:
        print(f"Hata: OpenVINO dışa aktarma başarısız oldu: {e}")

if __name__ == '__main__':
    export_models()
