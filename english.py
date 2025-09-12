import streamlit as st
import streamlit.components.v1 as components
import gtts
from gtts import gTTS
import os

# Direktori audio sementara
TEMP_AUDIO_DIR = "temp_audio"
if not os.path.exists(TEMP_AUDIO_DIR):
    os.makedirs(TEMP_AUDIO_DIR)

def text_to_speech(text):
    """Mengubah teks menjadi file audio MP3."""
    tts = gTTS(text=text, lang='en')
    path = f"{TEMP_AUDIO_DIR}/temp.mp3"
    with open(path, "wb") as f:
        tts.write_to_fp(f)
    return path

# Data kosakata
vocab_data = {
    "Hewan": [
        {'kata': 'Cat', 'terjemahan': 'Kucing', 'pelafalan': '(ket)'},
        {'kata': 'Dog', 'terjemahan': 'Anjing', 'pelafalan': '(dog)'},
        {'kata': 'Bird', 'terjemahan': 'Burung', 'pelafalan': '(berd)'},
    ],
    "Buah-buahan": [
        {'kata': 'Apple', 'terjemahan': 'Apel', 'pelafalan': '(epel)'},
        {'kata': 'Banana', 'terjemahan': 'Pisang', 'pelafalan': '(bænana)'},
        {'kata': 'Orange', 'terjemahan': 'Jeruk', 'pelafalan': '(orej)'},
    ]
}

# --------------------------
# ANTARMUKA UTAMA
# --------------------------
st.set_page_config(page_title="Kamus Kosakata Interaktif", layout="centered")

st.title("📚 Kamus Kosakata Inggris-Indonesia + 🎙️ Live STT")

st.sidebar.title("Pilih Topik")
topic_list = list(vocab_data.keys())
selected_topic = st.sidebar.radio("Daftar Topik", topic_list)

st.markdown("👇 Ucapkan kata dalam bahasa Inggris. Jika cocok, kata akan berubah hijau.")

# Tempat menyimpan hasil STT (session state agar bisa diakses Python)
if "recognized_text" not in st.session_state:
    st.session_state.recognized_text = ""

# --------------------------
# Komponen STT Realtime
# --------------------------
components.html(
    f"""
    <script>
    var recognition = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    recognition.onresult = function(event) {{
        var interim_transcript = '';
        var final_transcript = '';
        for (var i = event.resultIndex; i < event.results.length; ++i) {{
            if (event.results[i].isFinal) {{
                final_transcript += event.results[i][0].transcript;
            }} else {{
                interim_transcript += event.results[i][0].transcript;
            }}
        }}
        // Kirim hasil ke Streamlit
        var textInput = document.getElementById("stt_result");
        textInput.value = final_transcript;
        textInput.dispatchEvent(new Event("input", {{ bubbles: true }}));
    }};

    function startButton() {{ recognition.start(); }}
    function stopButton() {{ recognition.stop(); }}
    </script>

    <button onclick="startButton()">▶️ Start</button>
    <button onclick="stopButton()">⏹ Stop</button>
    <p id="status">🎤 Click Start to Speak</p>
    <input type="text" id="stt_result" style="display:none" />
    """,
    height=200,
)

# Text input tersembunyi sebagai jembatan data dari JS -> Python
recognized_text = st.text_input("STT Result (hidden)", key="recognized_text")

# --------------------------
# TABEL KOSAKATA
# --------------------------
st.subheader(f"Topik: {selected_topic}")
for i, vocab in enumerate(vocab_data[selected_topic]):
    word = vocab['kata']
    translation = vocab['terjemahan']
    pronunciation = vocab['pelafalan']

    # Cek apakah kata dikenali oleh STT
    if recognized_text.strip().lower() == word.lower():
        st.markdown(f"<p style='color:green; font-weight:bold'>{word} ✅</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p>{word} - *{translation}* {pronunciation}</p>", unsafe_allow_html=True)

    # Tombol TTS
    if st.button("🔊", key=f"tts_{word}_{i}"):
        audio_file_path = text_to_speech(word)
        with open(audio_file_path, "rb") as f:
            st.audio(f.read(), format='audio/mp3')
        os.remove(audio_file_path)
