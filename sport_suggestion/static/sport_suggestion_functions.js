// Form gönderme olayını dinle
// Kullanıcı formu gönderdiğinde bu fonksiyon çalışır
document.getElementById("sportForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Sayfanın yeniden yüklenmesini engelle

    // Form alanlarını al ve boş olup olmadıklarını kontrol et
    const age = document.getElementById("age").value.trim();
    const length = document.getElementById("length").value.trim();
    const weight = document.getElementById("weight").value.trim();

    // 'gender' değişkeni tanımlanmamış, eksik olabilir
    if (!age || !length || !weight || !gender) {
        alert("Lütfen tüm alanları doldurun."); // Kullanıcıya uyarı ver
        return;
    }

    // Negatif değer girişini engelle
    if(age < 0 || length < 0 || weight < 0){
        alert("Lütfen geçerli değerler girin.");
    }
   
    let formData = new FormData(this); // Form verilerini FormData nesnesine aktar

    // Verileri sunucuya gönder
    fetch("/", {
        method: "POST",
        body: formData
    })
    .then(response => response.text()) // Yanıtı metin olarak işle
    .then(data => {
        // Sunucudan gelen cevabı HTML içinde göster
        document.getElementById("response").innerHTML = `<p>${data}</p>`;
        
        // Sohbet butonunu görünür yap
        document.getElementById("chatButton").style.display = "block";
        
        // Formu sıfırla
        document.getElementById("sportForm").reset();
    })
    .catch(error => {
        console.error("Hata:", error); // Hata durumunda konsola yazdır
    });
});

// Kullanıcının mesaj giriş alanında "Enter" tuşuna basmasını dinle
document.getElementById("user-input").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Enter tuşunun varsayılan davranışını engelle
        sendMessage(); // Mesaj gönderme fonksiyonunu çağır
    }
});

// Mesaj gönderme fonksiyonu
function sendMessage() {
    const userInput = document.getElementById("user-input").value; // Kullanıcıdan alınan metni al
    if(!userInput.trim()){
        return; // Boş mesaj gönderilmesini engelle
    }
    
    // Kullanıcı mesajını sohbet kutusuna ekle
    const userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = userInput;
    const chatBox = document.getElementById("chat-box");
    chatBox.appendChild(userMessage);

    // Mesajı sunucuya gönder
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json()) // Yanıtı JSON formatında işle
    .then(data => {
        document.getElementById("user-input").value = ""; // Giriş alanını temizle
        
        // Bot yanıtını sohbet kutusuna ekle
        const botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        botMessage.innerHTML = data.response;
        chatBox.appendChild(botMessage);

        // Sohbet kutusunu en alta kaydır
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error("Hata:", error); // Hata oluşursa konsola yazdır
    });
}
