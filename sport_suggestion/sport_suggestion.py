from flask import Flask, request, render_template, jsonify
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import pickle
import numpy as np

app = Flask(__name__)

# Global değişken: Önerilen sporları burada saklayacağız
sport_recommendations = []
user_states = {}  # Kullanıcı durumlarını takip eden sözlük
user_physical_data = {}  # Kullanıcının fiziksel özelliklerini saklayan sözlük

# Load the model
MODEL_PATH = os.path.join('models', '12.03.2025_01.42.pickle')
with open(MODEL_PATH, 'rb') as f:
    model_sport = pickle.load(f)

# .env dosyasındaki değişkenleri yükle
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    print("API anahtarı bulunamadı. Lütfen .env dosyanızı kontrol edin.")
    exit()

# Hugging Face API istemcisini başlat
client = InferenceClient(
    provider="sambanova",
    api_key=HUGGINGFACE_API_KEY,
)

@app.route("/", methods=["GET", "POST"])
def sport_suggestion():
    global sport_recommendations  # Global değişkeni kullan
    global user_physical_data

    if request.method == "POST":
        # Form verilerini al
        gender = request.form.get("gender")
        age = float(request.form.get("age"))
        length = float(request.form.get("length"))
        weight = float(request.form.get("weight"))

        # BMI hesapla
        height_m = length / 100
        
        # Model için girdi verilerini hazırla
        gender_numeric = 1 if gender == "Erkek" else 0
        input_features = np.array([[int(gender_numeric), int(age), int(height_m), int(weight), 204]])
        user_physical_data = {
                "gender": gender,
                "age": age,
                "length": length,
                "weight": weight
            }
        print(f"User Physical Data: {user_physical_data}")

        try:
            # Model tahminini al
            proba = model_sport.predict_proba(input_features)

            # En yüksek olasılıklı 3 spor önerisini al
            top_3_indices = np.argsort(proba[0])[-3:][::-1]  
            top_3_classes = model_sport.classes_[top_3_indices]  
            top_3_probs = proba[0][top_3_indices]  

            # Global değişkende sakla (format: ["Spor1 (oran)", "Spor2 (oran)", "Spor3 (oran)"])
            sport_recommendations = [
                f"{i+1}. önerim: {top_3_classes[i]} ({top_3_probs[i]:.2%})"
                for i in range(3)
            ]

            print(f"Model Predictions:\n{sport_recommendations}")

            # HTML template'e liste olarak gönder
            return render_template("sport_llm.html", suggestions=sport_recommendations)
        except Exception as e:
            print(f"Model prediction error: {e}")
            return render_template("sport_llm.html", suggestions=[])

    # Formun bulunduğu sayfayı render et
    return render_template("sport_suggestion_index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global sport_recommendations
    global user_physical_data

    data = request.json
    user_input = data.get("message", "").strip().lower()
    user_id = data.get("user_id")  # Kullanıcıyı belirlemek için bir ID al

    if not user_input:
        return jsonify({"error": "Boş mesaj gönderilemez!"}), 400

    if not sport_recommendations:
        sport_recommendations = ["weightlifting-heavy_classes", "cardio-training", "yoga-flexibility"]

    # Kullanıcı durumu kontrolü: İlk mesajda önerilen sporlar hakkında konuş
    if user_id not in user_states:
        user_states[user_id] = "first_message"  # Kullanıcı için durum belirle

    suggestion_text = "\n".join([f"- {s}" for s in sport_recommendations])
    if user_states[user_id] == "first_message":
        context_message = (
            f"Kullanıcı için fiziksel özelliklerine göre {user_physical_data} ilk 3 spor:\n{suggestion_text}\n\n"
            "Bu öneriler, kullanıcının fiziksel özellikleri ve genel kondisyon seviyesine göre seçildi. "
            "Önerilen sporlar hakkında detaylı bilgi ver, nasıl yapılması gerektiğini açıkla ve kullanıcıya "
            "bu sporların sağladığı faydaları anlat. Kullanıcıya uygun egzersiz programları ve beslenme önerileri de sunabilirsin."
        )

        user_states[user_id] = "general_chat"  # Sonraki mesajlar için genel sohbete geç
    else:
        context_message = (
            f"Kullanıcı için önerilen sporları dikkate al:\n{suggestion_text}\n\n"
            f"Kullanıcının fiziksel özellikleri: {user_physical_data}.\n"
            "Bu bilgilere dayanarak, kullanıcının kondisyonunu geliştirmesi için uygun egzersiz programları öner.\n"
            "Önerilen sporlar hakkında ayrıntılı bilgi ver, bu sporları hangi kas gruplarını çalıştırdığına, "
            "ne tür bir fiziksel dayanıklılık gerektirdiğine ve hangi seviyedeki kişilerin bu sporlara uygun olduğuna değin.\n\n"
            "Spora yeni başlayanlar için ısınma hareketleri, antrenman sonrası toparlanma teknikleri ve beslenme ipuçları sun.\n"
            "Eğer kullanıcı kilo vermek, kas kazanmak veya esneklik geliştirmek gibi özel hedefler belirtiyorsa, "
            "bu hedeflere ulaşmak için en iyi antrenman stratejilerini paylaş.\n\n"
            "Spor yaparken sakatlıklardan korunma yöntemlerini anlat. Kullanıcının yaşına ve fiziksel özelliklerine göre "
            "esneme, güçlendirme ve hareket kabiliyetini artırıcı egzersizler öner.\n\n"
            "Sağlıklı bir yaşam tarzı geliştirmesi için uyku düzeni, stres yönetimi ve genel fitness ipuçları sun.\n"
            "Spor motivasyonu hakkında konuşarak, uzun vadeli başarı için düzenli egzersiz yapmanın psikolojik ve fiziksel faydalarını anlat.\n\n"
            "Eğer kullanıcı belirli bir spor dalına ilgi duyuyorsa, bu spor dalı hakkında detaylı bilgi ver ve antrenmanlarını nasıl optimize edebileceği konusunda önerilerde bulun.\n"
            "Kullanıcının merak ettiği diğer spor dalları veya farklı antrenman türleri hakkında da sohbet etmeye devam et."
        )


    try:
        messages = [
            {"role": "system", "content": context_message},
            {"role": "user", "content": user_input}
        ]
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct",
            messages=messages,
            max_tokens=500,
        )

        bot_response = completion.choices[0].message["content"].strip()

        print(f"User Input: {user_input}")
        print(f"LLaMA Response: {bot_response}")

        return jsonify({"response": format_response(bot_response)})
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Bir hata oluştu, lütfen daha sonra tekrar deneyin."}), 500

def format_response(response):
    # Metni HTML formatına dönüştür
    lines = response.split('*')
    formatted_response = ""
    for line in lines:
        if line.strip():
            if line.strip().endswith(':'):
                formatted_response += f"<h4>{line.strip()}</h4>"
            else:
                formatted_response += f"<p>{line.strip()}</p>"
    return formatted_response

if __name__ == "__main__":
    # Flask uygulamasını debug modda başlat
    app.run(debug=True)
