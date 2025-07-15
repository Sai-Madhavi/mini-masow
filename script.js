async function sendMessage() {
    const input = document.getElementById("userInput").value;
  
    const res = await fetch("http://localhost:5000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input })
    });
  
    const data = await res.json();
    document.getElementById("response").innerText = data.reply;
  
    // Speak the reply
    const msg = new SpeechSynthesisUtterance(data.reply);
    speechSynthesis.speak(msg);
  
    // Refresh chat history
    await loadHistory();
  }
  
  async function loadHistory() {
    const res = await fetch("/api/history");
    const history = await res.json();
    const container = document.getElementById("chatHistory");
    container.innerHTML = "<h3>Previous Chats:</h3>";
  
    history.forEach(chat => {
      const div = document.createElement("div");
      div.innerHTML = `<strong>You:</strong> ${chat.message}<br><strong>Baby Masow:</strong> ${chat.reply}<hr>`;
      container.appendChild(div);
    });
  }

  function playSong() {
    const songName = document.getElementById("songInput").value;
    const encoded = encodeURIComponent(songName);
    document.getElementById("youtubePlayer").src = `https://www.youtube.com/embed?search_query=${encoded}`;
  }


  async function uploadImage() {
    const fileInput = document.getElementById("imageInput");
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("image", file);
  
    const res = await fetch("/api/describe-image", {
      method: "POST",
      body: formData
    });
    const data = await res.json();
    document.getElementById("imageDescription").innerText = "I see: " + data.description;
  }

  function speak(text) {
    const msg = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(msg);
  }

  async function sendMessage() {
    const input = document.getElementById("userInput").value;
  
    const res = await fetch("http://localhost:5000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input })
    });
  
    const data = await res.json();
    document.getElementById("response").innerText = data.reply;
  
    // Speak the reply
    speak(data.reply);
  }

  async function searchWeb() {
    const query = document.getElementById("searchInput").value;
    const res = await fetch("/api/websearch", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });
    const data = await res.json();
    document.getElementById("searchResult").innerText = data.answer || "No answer found.";
  }
  
  function startListening() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.start();
  
    recognition.onresult = function(event) {
      const transcript = event.results[0][0].transcript;
      document.getElementById('userInput').value = transcript;
      sendMessage();
    };
  }
  
  // Call on page load
  window.onload = loadHistory;