import time
import os
import numpy as np
from ultralytics import YOLO

def run_benchmark():
    # Model yolları
    pt_path = 'runs/detect/kare_model_v3/weights/best.pt'
    # YOLO varsayılan dışa aktarım yolları
    onnx_path = 'runs/detect/kare_model_v3/weights/best.onnx'
    openvino_path = 'runs/detect/kare_model_v3/weights/best_openvino_model'
    
    configs = [
        {"name": "PyTorch (CPU)", "path": pt_path, "imgsz": 640},
        {"name": "PyTorch (CPU)", "path": pt_path, "imgsz": 320},
        {"name": "ONNX (CPU)", "path": onnx_path, "imgsz": 640},
        {"name": "ONNX (CPU)", "path": onnx_path, "imgsz": 320},
        {"name": "OpenVINO (CPU)", "path": openvino_path, "imgsz": 640},
        {"name": "OpenVINO (CPU)", "path": openvino_path, "imgsz": 320},
    ]
    
    print("\n--- HIZ TESTİ BAŞLATILIYOR (CPU) ---")
    results = []
    
    warmup_runs = 5
    benchmark_runs = 20
    
    for config in configs:
        path = config["path"]
        if not os.path.exists(path):
            print(f"Model bulunamadı (atlandı): {config['name']} @ {config['imgsz']}")
            continue
            
        print(f"Yükleniyor ve Test Ediliyor: {config['name']} @ {config['imgsz']}...")
        
        try:
            # Task 'detect' olarak belirtmek ve verbose=False yapmak çıktıları temiz tutar
            model = YOLO(path, task='detect')
            
            # Dummy resim oluştur (çözünürlüğe uygun)
            dummy_img = np.zeros((config["imgsz"], config["imgsz"], 3), dtype=np.uint8)
            
            # Isınma turları (warmup)
            for _ in range(warmup_runs):
                _ = model.predict(dummy_img, verbose=False)
                
            # Asıl ölçüm turları
            start_time = time.time()
            for _ in range(benchmark_runs):
                _ = model.predict(dummy_img, verbose=False)
            end_time = time.time()
            
            total_time = end_time - start_time
            avg_latency = (total_time / benchmark_runs) * 1000  # milisaniye
            fps = benchmark_runs / total_time
            
            results.append({
                "Format": config["name"],
                "imgsz": config["imgsz"],
                "latency": avg_latency,
                "fps": fps
            })
        except Exception as e:
            print(f"Hata: {config['name']} test edilirken hata oluştu: {e}")
        
    if not results:
        print("\nHiçbir model test edilemedi. Lütfen 'optimize.py' betiğini çalıştırarak modelleri üretin.")
        return
        
    # Sonuçları ekrana yazdır
    print("\n" + "="*70)
    print(f" {'MODEL FORMATI':<22} | {'ÇÖZÜNÜRLÜK':<10} | {'ORT. GECİKME (ms)':<18} | {'FPS':<10}")
    print("-"*70)
    for res in results:
        print(f" {res['Format']:<22} | {res['imgsz']:<10} | {res['latency']:<18.2f} | {res['fps']:<10.2f}")
    print("="*70)
    print("\n* İHA canli kameranız veya video çıkarımlarınız için en yüksek FPS ve en düşük gecikmeye sahip modeli tercih edin.")

if __name__ == '__main__':
    run_benchmark()
