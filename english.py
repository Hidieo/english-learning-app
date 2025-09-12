import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Kamus Kosakata", layout="wide")

st.title("📚 Kamus Kosakata Inggris-Indonesia — TTS & STT")

# Daftar vocabulary (bisa diganti sesuai kebutuhan)
vocab_list = [
    {"en": "cat", "id": "kucing"},
    {"en": "dog", "id": "anjing"},
    {"en": "apple", "id": "apel"},
    {"en": "banana", "id": "pisang"}
]

# Konversi ke JS
vocab_js = str([v["en"] for v in vocab_list]).replace("'", '"')

# Render UI
for vocab in vocab_list:
    en_word = vocab["en"]
    id_word = vocab["id"]

    st.markdown(f"### {en_word.capitalize()} — *{id_word}*")

    components.html(
        f"""
        <div style="margin-bottom:15px;">
            <!-- Tombol TTS -->
            <button onclick="speakWord('{en_word}')">🔊 TTS</button>
            
            <!-- Tombol STT -->
            <button onclick="startRecognition('{en_word}')">🎙️ STT</button>
            <span id="result_{en_word}" style="margin-left:10px; font-weight:bold; color:gray;"></span>
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
                var resultElem = document.getElementById("result_" + targetWord);

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
