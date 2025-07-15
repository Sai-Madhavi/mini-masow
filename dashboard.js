async function loadDashboard() {
    const res = await fetch("/dashboard");
    const data = await res.json();
  
    document.getElementById("userEmail").innerText = data.email;
    document.getElementById("totalChats").innerText = data.total_chats;
  
    if (data.last_chat) {
      document.getElementById("lastMessage").innerText = data.last_chat.message;
      document.getElementById("lastReply").innerText = data.last_chat.reply;
    }
  
    // Load recent chats
    const chatList = document.getElementById("chatList");
    const historyRes = await fetch("/api/history");
    const history = await historyRes.json();
  
    chatList.innerHTML = "";
    history.slice(0, 5).forEach(chat => {
      const li = document.createElement("li");
      li.innerHTML = `<strong>You:</strong> ${chat.message}<br><strong>Baby Masow:</strong> ${chat.reply}`;
      chatList.appendChild(li);
    });
  
    // Generate suggestions
    const suggestionList = document.getElementById("suggestions");
    suggestionList.innerHTML = "";
  
    const keywords = {};
    history.forEach(chat => {
      const words = chat.message.toLowerCase().split(/\s+/);
      words.forEach(word => {
        if (word.length > 3) keywords[word] = (keywords[word] || 0) + 1;
      });
    });
  
    const topKeywords = Object.entries(keywords)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([word]) => word);
  
    if (topKeywords.length) {
      topKeywords.forEach(keyword => {
        const li = document.createElement("li");
        li.innerText = `You might like more about "${keyword}"`;
        suggestionList.appendChild(li);
      });
    } else {
      suggestionList.innerHTML = "<li>No suggestions yet — start chatting!</li>";
    }
  }
  
  window.onload = loadDashboard;