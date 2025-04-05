# 🎉 Sport_Suggestion Projesine Hoş Geldiniz!

![Madalya Görseli](/assets/madalya.PNG)

🎉 **Şöbiyet Takımı olarak 1. olduk!**  
Gençlik ve Spor Bakanlığı tarafından düzenlenen Yapay Zeka Hackathonu'nda, "Kişiselleştirilmiş Spor Öneri Platformu" projemizle birincilik elde ettik.

🔗 Yarışma hakkında detaylı bilgiye buradan ulaşabilirsiniz:  
[https://genchackathon.gsb.gov.tr/guncel-yarismalar/index.html](https://genchackathon.gsb.gov.tr/guncel-yarismalar/index.html)

![Proje Görseli](/assets/derece.png)


📄 Proje tanıtım dokümanını incelemek isterseniz [buradan PDF'e ulaşabilirsiniz.](../assets/Şöbiyet%20Grubu%20-%20Spor%20Öneri%20Platformu%20Heckhaton%20Proje%20Raporu.pdf)

Bu dokümanda; projenin amacı, hedef kitlesi, kullanılan teknolojiler, veri seti süreci, modelleme ve değerlendirme adımları detaylı bir şekilde açıklanmıştır.

---

## 📌 Proje Amacı
Bu proje, **genç bireylerin spora başlama kararı almasını kolaylaştırmak** amacıyla onların fiziksel verilerine göre uygun spor dallarını öneren, aynı zamanda bir dil modeliyle spor üzerine sohbet edebilecekleri bir platformdur.

## **🎥Uygulama Kullanımı (GIF)**

Aşağıdaki GIF ile uygulamanın nasıl çalıştığını hızlıca görebilirsiniz:

![Uygulama Kullanımı](/assets/video.gif)


## 🚀 Projeyi Çalıştırma Adımları

1. **Model Eğitimi**
   - `MLE_scripts` klasöründeki README dosyasını okuyunuz.
   - Model eğitimi için gerekli yönergeleri burada bulacaksınız.
   - Eğitimi Docker üzerinde yapacağınızdan dolayı **spesifik kütüphane kurulumu gerekmemektedir.**
   - Eğitilen `pickle` modelinizi `sport_suggestion/models` klasörünün içine koymayı unutmayınız.
   - [Model Eğitim README'ine Gitmek İçin Tıklayın](https://github.com/AysenurYrr/sport_suggestion/tree/main/MLE_scripts)

2. **HuggingFace API Key Alın**
   - HuggingFace hesabı oluşturun: https://huggingface.co
   - Settings > Access Tokens kısmından yeni bir `read` yetkisine sahip token oluşturun.

3. **.env Dosyasını Düzenleyin**
   - Proje dizininde `.env` adında bir dosya oluşturun.
   - İçerisine şu formatta API anahtarınızı yazın:
     ```
     HF_API_KEY=buraya_sizin_anahtarınız
     ```

4. **Projeyi Çalıştırın**
   ```bash
   python sport_suggestion.py

## 📂 sport_suggestion.py Nedir?

`sport_suggestion.py` dosyası, Flask kullanılarak geliştirilmiş olan arka uç (backend) yapısını barındırır. Bu dosya, hem kullanıcıdan alınan verilerin işlenmesini hem de Gemini API ile yapılan spor temalı sohbet işlemlerini yürütür.

### 🎯 Temel Özellikleri:
- Kullanıcı, HTML form aracılığıyla **yaş, boy, kilo ve cinsiyet** bilgilerini girer.
- Flask, bu verileri alarak eğitimli makine öğrenmesi modeline (pickle dosyası) gönderir.
- Model, kullanıcının fiziksel verilerine göre en uygun **10 farklı spor branşını** önerir.
- Ardından kullanıcı, Gemini API ile entegre edilmiş **chat arayüzüne** yönlendirilir.
- Chat arayüzünde, kullanıcı yalnızca spor temalı sohbetler yapabilir. Spor dışı konulara yönelmemesi için **anahtar kelime kısıtlamaları** eklenmiştir.

### 🔐 Güvenlik Özellikleri:
- Gemini API key `.env` dosyasından okunur, bu sayede kod içerisinde açık şekilde yer almaz.
- Kullanıcı verileri hiçbir şekilde sunucuda tutulmaz, gizlilik ve anonimlik sağlanır.

### 🧠 Kütüphaneler:
- `Flask` → Web sunucusu
- `os` → Ortam değişkenleri ile çalışma
- `pickle` → Model yükleme
- `dotenv` → .env dosyasını okumak için
- `pandas`, `numpy` → Veri işleme

---

## 🔍 Yöntemler ve Kullanılan Modeller

Makine öğrenmesi tarafında:

- **Veri Kümesi:** 1896-2016 yılları arası olimpiyatlara katılmış 270K+ sporcu verisi
- **Özellikler:** Yaş, boy, kilo, cinsiyet
- **Modeller:** 
  - Logistic Regression
  - SVM
  - Gradient Boosting
  - Naive Bayes
  - ✅ **Random Forest** (en iyi doğruluk & hız dengesi nedeniyle seçildi)

- **Model Performansı:**
  - Temel RF modelinin doğruluğu: `0.2627`
  - Yeni özelliklerle geliştirilen modelin doğruluğu: `0.6706`

---

## 🔮 Gelecekte Neler Planlıyoruz?
- Kişinin bulunduğu şehre göre **yakın gençlik merkezlerinin** listelenmesi
- LLM ile **kişilik analizine dayalı** daha spesifik spor önerileri
- Uygulamanın **Biz mobil uygulamasına entegre edilmesi**
