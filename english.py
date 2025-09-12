import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="English Learning App", layout="wide")

st.title("🎤 English Learning App")

# Kode HTML + JS dimasukkan ke dalam string
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>English Learning App</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background: #f8f9fa; }
    .topic-btn {
      width: 100%;
      margin: 5px 0;
      font-size: 1rem;
      font-weight: 500;
      padding: 12px;
      border-radius: 12px;
      transition: all 0.3s ease;
    }
    .topic-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
    }
    #result {
      background: #ffffff;
      border-radius: 12px;
      padding: 15px;
      min-height: 120px;
      margin-top: 15px;
      box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    }
    .highlight {
      color: green;
      font-weight: bold;
    }
    footer {
      margin-top: 30px;
      text-align: center;
      font-size: 0.9rem;
      color: #6c757d;
    }
  </style>
</head>
<body>

<div class="container py-4">
  <h1 class="text-center mb-4">🎤 English Learning App</h1>

  <!-- Menu 16 Topic -->
  <div class="row row-cols-2 row-cols-md-4 g-3">
    <div class="col"><button class="btn btn-outline-primary topic-btn" onclick="setTopic(1)">Topic 1: Greeting</button></div>
    <div class="col"><button class="btn btn-outline-primary topic-btn" onclick="setTopic(2)">Topic 2: Numbers</button></div>
    <div class="col"><button class="btn btn-outline-primary topic-btn" onclick="setTopic(3)">Topic 3: Hotel Jobs</button></div>
    <div class="col"><button class="btn btn-outline-primary topic-btn" onclick="setTopic(4)">Topic 4: Directions</button></div>
    <div class="col"><button class="btn btn-outline-primary topic-btn" onclick="setTopic(5)">Topic 5: Reservations</button></div>
    <div class="col"><button class="btn btn-outline-primary topic-btn" onclick="setTopic(6)">Topic 6: Check-in/out</button></div>
    <div class="col"><button class="btn btn-outline-primary topic-btn" onclick="setTopic(7)">Topic 7: Hotel Facilities</button></div>
    <div class="col"><button class="btn btn-outline-primary topic-btn" onclick="setTopic(8)">Topic 8: Food & Drinks</button></div>
    <div class="col"><button class="btn btn-outline-primary topic-btn" onclick="setTopic(9)">Topic 9</button></div>
    <div class="col"><button class="btn btn-outline-primary topic-btn" onclick="setTopic(10)">Topic 10</button></div>
    <div class="col"><button class="btn btn-outline-primary topic-btn" onclick="setTopic(11)">Topic 11</button></div>
    <div class="col"><button class="btn btn-outline-primary topic-btn" onclick="setTopic(12)">Topic 12</button></div>
    <div class="col"><button class="btn btn-outline-primary topic-btn" onclick="setTopic(13)">Topic 13</button></div>
    <div class="col"><button class="btn btn-outline-primary topic-btn" onclick="setTopic(14)">Topic 14</button></div>
    <div class="col"><button class="btn btn-outline-primary topic-btn" onclick="setTopic(15)">Topic 15</button></div>
    <div class="col"><button class="btn btn-outline-primary topic-btn" onclick="setTopic(16)">Topic 16</button></div>
  </div>

  <!-- Hasil Speech -->
  <div id="result" class="mt-4">
    <p class="text-muted">🎙️ Hasil ucapan Anda akan muncul di sini...</p>
  </div>

  <!-- Tombol Record -->
  <div class="d-flex justify-content-center mt-3">
    <button class="btn btn-success btn-lg px-4" onclick="startRecognition()">🎙️ Start Speaking</button>
  </div>

  <footer>English Learning App © 2025</footer>
</div>

<script>
  let vocabularySets = {
    1: ["hello", "hi", "good morning", "good afternoon", "good evening", "how are you"],
    2: ["one", "two", "three", "four", "five", "ten", "twenty"],
    3: ["receptionist", "manager", "chef", "waiter", "bellboy"],
    4: ["left", "right", "straight", "corner", "block"],
    5: ["reservation", "booking", "confirm", "guest"],
    6: ["check-in", "check-out", "room key", "passport"],
    7: ["pool", "gym", "spa", "restaurant", "bar"],
    8: ["breakfast", "lunch", "dinner", "coffee", "tea"]
  };

  let currentTopic = 1;

  function setTopic(topic) {
    currentTopic = topic;
    document.getElementById("result").innerHTML = `<p class="text-primary">Topic ${topic} dipilih. Silakan bicara...</p>`;
  }

  function highlightWords(text) {
    let words = text.split(/\\s+/);
    return words.map(w => {
      let cleanWord = w.replace(/[.,!?;:]/g, "").toLowerCase();
      if (vocabularySets[currentTopic]?.includes(cleanWord)) {
        return `<span class="highlight">${w}</span>`;
      } else {
        return w;
      }
    }).join(" ");
  }

  function startRecognition() {
    if (!('webkitSpeechRecognition' in window)) {
      alert("Browser tidak mendukung Speech Recognition!");
      return;
    }
    let recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = function(event) {
      let transcript = event.results[0][0].transcript;
      document.getElementById("result").innerHTML = highlightWords(transcript);
    };
  }
</script>
</body>
</html>
"""

# Tampilkan HTML di Streamlit
components.html(html_code, height=800, scrolling=True)
