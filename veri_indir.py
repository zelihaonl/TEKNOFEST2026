from roboflow import Roboflow
import os

# 1. API Anahtarı (Güvenlik için ortam değişkeninden alınır, yoksa varsayılan atanır)
api_key = os.getenv("ROBOFLOW_API_KEY", "vGrQfFAjdWfDDPA2JLhe")
rf = Roboflow(api_key=api_key)

# 2. Proje Bilgileri (Roboflow adresindeki proje kimlikleri)
project = rf.workspace("teknofest-cnqdf").project("altay-kare-tanimlama-wgvb5")

# 3. Veri Setini İndir
dataset = project.version(2).download("yolov8", location="IHA_Veri_Seti")

print("\n--- BAŞARILI ---")
print("Veri seti 'IHA_Veri_Seti' adıyla klasöre indirildi.")