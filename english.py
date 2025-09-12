import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Kamus Kosakata", layout="wide")

st.title("📚 Kamus Kosakata Inggris-Indonesia — TTS & STT")

# ======================
# Daftar 16 Topik
# ======================
topics = {
    "Topic 1 - Greeting & Expression": [
        {"en": "Good morning", "ph": "Gud mo-ning", "id": "Selamat pagi"},
        {"en": "Good afternoon", "ph": "Gud af-ter-nun", "id": "Selamat siang"},
        {"en": "Good evening", "ph": "Gud i-vning", "id": "Selamat malam"},
        {"en": "Sir", "ph": "Ser", "id": "Tuan"},
        {"en": "Madam", "ph": "Medem", "id": "Nyonya/Ibu"},
        {"en": "How are you?", "ph": "Hau ar yu?", "id": "Apa kabar"},
        {"en": "How can I help you?", "ph": "Hau ken ai help yu", "id": "Apa yang bisa saya bantu"},
        {"en": "May I have your name?", "ph": "Mei ai hev yor neim", "id": "Boleh saya tahu nama anda?"},
        {"en": "May I help with your luggage?", "ph": "Mei ai help wit yor lagij", "id": "Bolehkah saya membantu koper anda?"},
        {"en": "Please follow me", "ph": "Plis folou mi", "id": "Silahkan ikuti saya"},
        {"en": "Enjoy your stay", "ph": "Enjoi yor stei", "id": "Selamat menikmati masa menginap anda"},
        {"en": "Nice to meet you", "ph": "Nais tu mit yu", "id": "Senang bertemu anda"},
        {"en": "You’re welcome", "ph": "Yor welkom", "id": "Sama-sama"},
        {"en": "My pleasure", "ph": "Mai plezur", "id": "Senang bisa membantu"},
    ],
    "Topic 2a - Numbers": [
        {"en": "one", "ph": "wan", "id": "1"},
        {"en": "two", "ph": "twu", "id": "2"},
        {"en": "three", "ph": "thri", "id": "3"},
        {"en": "four", "ph": "for", "id": "4"},
        {"en": "five", "ph": "faiv", "id": "5"},
        {"en": "six", "ph": "siks", "id": "6"},
        {"en": "seven", "ph": "seven", "id": "7"},
        {"en": "eight", "ph": "eit", "id": "8"},
        {"en": "nine", "ph": "nain", "id": "9"},
        {"en": "ten", "ph": "ten", "id": "10"},
        {"en": "eleven", "ph": "ilevn", "id": "11"},
        {"en": "twelve", "ph": "twelv", "id": "12"},
        {"en": "thirteen", "ph": "thertin", "id": "13"},
        {"en": "fourteen", "ph": "forti:n", "id": "14"},
        {"en": "fifteen", "ph": "fifti:n", "id": "15"},
        {"en": "sixteen", "ph": "sixti:n", "id": "16"},
        {"en": "seventeen", "ph": "seventi:n", "id": "17"},
        {"en": "eighteen", "ph": "eiti:n", "id": "18"},
        {"en": "nineteen", "ph": "nainti:n", "id": "19"},
        {"en": "twenty", "ph": "twenti", "id": "20"},
    ],
    # tambahkan Topic 2b, 2c, 2d, dst...
}

# ======================
# Menu pilih topik
# ======================
topic_choice = st.sidebar.radio("📌 Pilih Topik", list(topics.keys()))

st.subheader(f"📖 {topic_choice}")

# ======================
# Tampilkan Vocabulary
# ======================
vocab_list = topics[topic_choice]

for vocab in vocab_list:
    en_word = vocab["en"]
    ph_word = vocab["ph"]
    id_word = vocab["id"]

    st.markdown(f"### {en_word} ({ph_word}) — *{id_word}*")

    components.html(
        f"""
        <div style="margin-bottom:15px;">
            <!-- Tombol TTS -->
            <button onclick="speakWord('{en_word}')">🔊 TTS</button>
            
            <!-- Tombol STT -->
            <button onclick="startRecognition('{en_word}')">🎙️ STT</button>
            <span id="result_{en_word.replace(" ", "_")}" style="margin-left:10px; font-weight:bold; color:gray;"></span>
        </div>

        <script>
        // TTS
        function speakWord(word) {{
            var utterance = new SpeechSynthesisUtterance(word);
            utterance.lang = "en-US";
            speechSynthesis.speak(utterance);
        }}

        // STT
        function startRecognition(targetWord) {{
            var recognition = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = "en-US";
            recognition.start();

            recognition.onresult = function(event) {{
                var transcript = event.results[0][0].transcript.toLowerCase();
                var resultElem = document.getElementById("result_" + targetWord.replace(/ /g,"_"));

                if (transcript.includes(targetWord.toLowerCase())) {{
                    resultElem.innerHTML = "✅ Benar (" + transcript + ")";
                    resultElem.style.color = "green";
                }} else {{
                    resultElem.innerHTML = "❌ Salah (" + transcript + ")";
                    resultElem.style.color = "red";
                }}
            }};
        }}
        </script>
        """,
        height=80,
    )
