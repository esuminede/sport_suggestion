from flask import Flask, request, render_template, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)

# .env dosyasındaki değişkenleri yükle
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Google Gemini AI modelini API anahtarı ile yapılandır
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Sporla ilgili temel kelimeler kümesi
SPORT_KEYWORDS = {"spor", "fitness", "workout", "egzersiz", "koşu", "gym", "yoga", "futbol", "basketbol", "atletizm", "koşu", "yüzme", "voleybol", "karate", "judo",
                  "eskrim", "boks", "kickboks", "muaythai", "tenis", "badminton", "golf", "kayak", "kano", "rafting", "dağcılık", "kampçılık", "bisiklet", "paten", "kaykay"}

@app.route("/", methods=["GET", "POST"])
def sport_suggestion():
    if request.method == "POST":
        # Form verilerini al
        gender = request.form.get("gender")
        age = request.form.get("age")
        length = request.form.get("length")
        weight = request.form.get("weight")

        # Basit bir spor öneri mekanizması
        if gender == "Kadın":
            suggestion = "Yoga veya Pilates"
        else:
            suggestion = "Futbol veya Ağırlık Çalışması"

        return render_template("sport_llm.html", suggestion=suggestion)

    # Formun bulunduğu sayfayı render et
    return render_template("sport_suggestion_index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message").lower()

    # Boş mesaj gönderilmesini engelle
    if not user_input:
        return jsonify({"error": "Boş mesaj gönderilemez!"}), 400

    # Kullanıcının mesajının sporla ilgili olup olmadığını kontrol et
    if not any(word in user_input for word in SPORT_KEYWORDS):
        return jsonify({"response": "Bu sohbet sadece spor hakkında konuşmak içindir. Lütfen sporla ilgili bir soru sorun!"})

    try:
        # Google Gemini AI modeli ile mesajı işle
        response = model.generate_content(f"Sen bir spor asistanısın. Sadece spor hakkında konuşabilirsin. {user_input}")
        bot_response = format_response(response.text.strip())
        
        # Kullanıcı girdisini ve model yanıtını konsola yazdır
        print(f"User Input: {user_input}")
        print(f"Gemini Response: {bot_response}")
        
        return jsonify({"response": bot_response})
    except Exception as e:
        # Beklenmedik hataları yakala ve hata mesajı dön
        print(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

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
