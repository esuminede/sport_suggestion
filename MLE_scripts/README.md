## Ön Koşullar
Projeyi çalıştırmadan önce, geliştirme ortamınızı uygun şekilde yapılandırmanız gerekmektedir.
Eğer Docker veya MLFlow kurulumu sırasında sorun yaşarsanız, Python ve Git kullanarak yerel makinenizde doğrudan çalışabilirsiniz.

## 🛠️ Geliştirme Ortamını Hazırlama
### 1️⃣ **VS Code Kurulumu**  
- [VS Code'u buradan indirin](https://code.visualstudio.com/Download).  
- Kurulum tamamlandıktan sonra **File -> Add Folder to Workspace** seçeneğiyle klonladığınız proje klasörünü açın.  
- Terminali açarak (`Terminal -> New Terminal`) **Python dosyalarınızı çalıştırabilirsiniz**.  

### 2️⃣ **Docker Kurulumu (İsteğe Bağlı)**  
- [Docker'ı buradan indirin](https://www.docker.com/products/docker-desktop).  
- Windows veya Mac için uygun sürümü indirerek kurulum adımlarını takip edin.  
- Docker’ın çalıştığını doğrulamak için terminalde şu komutu çalıştırabilirsiniz:  
```bash
  docker --version
```

### 3️⃣ MLFlow Kurulumu (İsteğe Bağlı)
ML modellerinin takibini ve yönetimini sağlayan MLFlow'u yüklemek için:

```bash
pip install mlflow
```

## 🐳 Docker Desktop Kurulumu Ayrıntılı

Docker Desktop'u yüklemek oldukça basit bir işlemdir. **Docker'ın resmi web sitesine** giderek ([Docker İndirme Sayfası](https://www.docker.com/products/docker-desktop)), işletim sisteminize uygun sürümü seçin. Docker Desktop, **Windows ve Mac** için mevcuttur.  

**1️⃣ Kurulum Adımları:**  
- Uygun sürümü indirin.  
- İndirilen yükleyiciyi çalıştırın ve ekrandaki talimatları takip edin.  

 **2️⃣ Kurulum Tamamlandıktan Sonra:**  
- Docker Desktop'u açarak çalıştığını doğrulayın.  
- Uygulamalar veya programlar listesinde **Docker Desktop**’u görebilirsiniz.  
- Docker, siz bir komut çalıştırana kadar arka planda bekleyecektir.  

Docker Desktop, **Docker komut satırını bir arayüzle birleştirerek** işlemleri kolaylaştırır. Böylece, **konteynerleri (containers), imajları (images) ve ağları (networks)** doğrudan masaüstünüzden yönetebilirsiniz.  

⚠️ **Önemli Not:**  
Docker’ı kullanabilmek için **bilgisayarınızın BIOS ayarlarında sanallaştırmanın (virtualization) etkin olması gerekmektedir**. Eğer kurulum sırasında bir sorun yaşarsanız:  
- **BIOS ayarlarını kontrol edin.**  
- **Docker'ın resmi hata giderme kılavuzuna başvurun.**  


## Proje Yapısı:

Proje modüler olarak geliştirilmiştir

```
MLE_basic_example
├── data                      
│   ├── inference.csv
│   └── train.csv
├── data_process              
│   ├── data_generation.py
│   └── __init__.py           
├── inference                 
│   ├── Dockerfile
│   ├── run.py
│   └── __init__.py
├── models                    
│   └── various model files
├── training                 
│   ├── Dockerfile
│   ├── train.py
│   └── __init__.py
├── utils.py                  
├── settings.json             
├── event_categories.json
├── settings.json
└── README.md

```

## Settings:
Projenin tüm ayarları **`settings.json`** dosyası üzerinden yönetilmektedir.  
Bu dosya, projenin davranışını kontrol eden önemli değişkenleri saklar.  

📌 **İçeriğinde bulunabilecek ayarlar:**  
- **Dosya yolları** (veri setleri, modeller vb.)  
- **Sabit değerler**  
- **Makine öğrenmesi modelleri için hiperparametreler**  
- **Farklı çalışma ortamlarına özel ayarlar**  

🔍 **Projeyi çalıştırmadan önce:**  
Tüm **yolların ve parametrelerin doğru şekilde tanımlandığından** emin olun.  

## Veri:
Veri, her **Makine Öğrenmesi** projesinin temel taşıdır.  
Veri oluşturmak için **`data_process/data_generation.py`** betiğini kullanabilirsiniz.  
Oluşturulan veri, **modelin eğitilmesi** ve **çıkarım aşamasında test edilmesi** için kullanılır.  

**Sorumlulukların ayrılması** prensibine uygun olarak, **veri üretimi yalnızca bu betik tarafından yönetilmektedir**.  

## Training:

1. Modeli Docker ile train etme: 

```bash
docker build -f ./training/Dockerfile --build-arg settings_name=settings.json -t training_image .
```

## Inference:
Model eğitildikten sonra çalıştırılması planlanmaktadır ama maalesef ki inference tamamlanamadı.

- Build inference Docker image şu şekildedir:
```bash
docker build -f ./inference/Dockerfile --build-arg model_name=<model_name>.pickle --build-arg settings_name=settings.json -t inference_image .
```