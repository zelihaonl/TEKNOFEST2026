import cv2
import os
import time
from ultralytics import YOLO

def canli_tahmin():
    # 1. En uygun modeli seç (Sırasıyla OpenVINO, ONNX, PyTorch kontrol edilir)
    openvino_path = 'runs/detect/kare_model_v3/weights/best_openvino_model'
    onnx_path = 'runs/detect/kare_model_v3/weights/best.onnx'
    pt_path = 'runs/detect/kare_model_v3/weights/best.pt'
    
    model_path = pt_path
    if os.path.exists(openvino_path):
        model_path = openvino_path
        print(f"Yüksek Hızlı OpenVINO modeli seçildi: {model_path}")
    elif os.path.exists(onnx_path):
        model_path = onnx_path
        print(f"Optimize ONNX modeli seçildi: {onnx_path}")
    else:
        print(f"Uyarı: Optimize model bulunamadı, standart PyTorch modeli kullanılıyor: {pt_path}")
        if not os.path.exists(pt_path):
            print("Hata: Ağırlık dosyaları bulunamadı! Lütfen runs/detect/kare_model_v3 klasörünü kontrol edin.")
            return

    # Modeli Yükle
    model = YOLO(model_path, task='detect')

    # 2. Test videosunu belirle
    video_path = 'deneme videosu.mp4'
    if not os.path.exists(video_path):
        print(f"Hata: Test videosu bulunamadı! Yol: {video_path}")
        print("Lütfen proje dizininde bir test videosu bulundurun veya yolunu koddan güncelleyin.")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Hata: Video dosyası açılamadı.")
        return

    # Çıkarım Ayarları (Hızlandırma için ayarlanabilir)
    img_size = 640        # ONNX 640 hem hızlı hem de en doğru sonucu verir
    conf_threshold = 0.40 # Güven eşiği daha fazla hedef tespiti için %40 yapıldı
    vid_stride = 1        # Ek hız için 2 veya 3 yapılabilir (kare atlama)

    print("\n--- CANLI TEST BAŞLATILDI ---")
    print("Klavye Kontrolleri:")
    print("  [Space]  -> Duraklat / Devam Et")
    print("  [q]      -> Çıkış")
    
    paused = False
    
    # FPS hesaplama değişkenleri
    prev_time = 0
    
    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print("Video sonuna gelindi veya okunamadı. Tekrar başlatılıyor...")
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            
            # Kare atlama simülasyonu (vid_stride)
            frame_id = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            if frame_id % vid_stride != 0:
                continue

            # Model Tahmini
            start_inference = time.time()
            results = model.predict(source=frame, conf=conf_threshold, imgsz=img_size, verbose=False)
            end_inference = time.time()
            
            # FPS Hesaplama (Tüm döngü süresine göre)
            current_time = time.time()
            fps = 1 / (current_time - prev_time) if prev_time != 0 else 0
            prev_time = current_time
            
            # YOLO Çizimlerini Al
            annotated_frame = results[0].plot()
            
            # Çıkarım Gecikmesi (ms)
            inference_ms = (end_inference - start_inference) * 1000
            
            # Ekrana FPS ve Tespit Edilen Hedef Sayısını Yazdır
            h, w, _ = annotated_frame.shape
            cv2.rectangle(annotated_frame, (10, 10), (280, 110), (0, 0, 0), -1) # Bilgi paneli arka planı
            
            cv2.putText(annotated_frame, f"Model: {os.path.basename(model_path)}", (20, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(annotated_frame, f"FPS: {fps:.1f}", (20, 55), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Gecikme: {inference_ms:.1f} ms", (20, 75), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            cv2.putText(annotated_frame, f"Hedefler: {len(results[0])} adet", (20, 95), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # Görseli göster
            cv2.imshow("IHA YOLOv11 Canli Tespit ve Hiz Testi", annotated_frame)

        # Tuş kontrollerini dinle
        key = cv2.waitKey(1) & 0xFF
        
        # Pencere kapatma (X) butonuna basıldıysa veya q/ESC tuşuna basıldıysa çık
        try:
            if cv2.getWindowProperty("IHA YOLOv11 Canli Tespit ve Hiz Testi", cv2.WND_PROP_VISIBLE) < 1:
                break
        except Exception:
            pass

        if key == ord('q') or key == 27: # q veya ESC
            break
        elif key == ord(' '): # Spacebar
            paused = not paused
            if paused:
                print("Durduruldu. Devam etmek için tekrar [Space] tuşuna basın.")
            else:
                print("Devam ediliyor...")
                prev_time = time.time() # FPS sapmasını önlemek için süreyi sıfırla

    cap.release()
    cv2.destroyAllWindows()
    print("--- CANLI TEST SONLANDIRILDI ---")

if __name__ == '__main__':
    canli_tahmin()
