document.getElementById("sportForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Sayfanın yeniden yüklenmesini engelle

    // Form alanlarını kontrol et
    const age = document.getElementById("age").value.trim();
    const length = document.getElementById("length").value.trim();
    const weight = document.getElementById("weight").value.trim();

    if (!age || !length || !weight || !gender) {
        alert("Lütfen tüm alanları doldurun.");
        return;
    }
    if(age < 0 || length < 0 || weight < 0){
        alert("Lütfen geçerli değerler girin.");
    }
   
    let formData = new FormData(this);

    fetch("/", {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById("response").innerHTML = `<p>${data}</p>`;
        // Show the chat button after displaying the suggestion
        document.getElementById("chatButton").style.display = "block";
        document.getElementById("sportForm").reset();
    })
    .catch(error => {
        console.error("Hata:", error);
    });
});

document.getElementById("user-input").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Enter tuşunun varsayılan davranışını engelle
        sendMessage(); // Mesaj gönderme fonksiyonunu çağır
    }
});

function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    if(!userInput.trim()){
        return;
    }
    const userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = userInput;
    const chatBox = document.getElementById("chat-box");
    chatBox.appendChild(userMessage);

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
        
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("user-input").value = ""; 
        const botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        botMessage.innerHTML = data.response;
        chatBox.appendChild(botMessage);

        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error("Hata:", error);
    });
}

