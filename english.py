# -*- coding: utf-8 -*-
import streamlit as st
import gtts
from gtts import gTTS
import os
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode

# Tentukan direktori untuk menyimpan file audio sementara
TEMP_AUDIO_DIR = "temp_audio"
if not os.path.exists(TEMP_AUDIO_DIR):
    os.makedirs(TEMP_AUDIO_DIR)

# --- FUNGSI-FUNGSI UTAMA ---

def text_to_speech(text):
    """Mengubah teks menjadi file audio MP3."""
    tts = gTTS(text=text, lang='en')
    with open(f"{TEMP_AUDIO_DIR}/temp.mp3", "wb") as f:
        tts.write_to_fp(f)
    return f"{TEMP_AUDIO_DIR}/temp.mp3"

# --- SPEECH TO TEXT PROCESSOR ---

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.text = ""

    def recv_audio(self, frame):
        audio = frame.to_ndarray().tobytes()
        audio_data = sr.AudioData(audio, frame.sample_rate, 2)
        try:
            result = self.recognizer.recognize_google(audio_data, language="en-US")
            self.text = result
        except:
            pass
        return frame

# --- DATA KOSAKATA ---

vocab_data = {
    "Hewan": [
        {'kata': 'Cat', 'terjemahan': 'Kucing', 'pelafalan': '(ket)'},
        {'kata': 'Dog', 'terjemahan': 'Anjing', 'pelafalan': '(dog)'},
        {'kata': 'Bird', 'terjemahan': 'Burung', 'pelafalan': '(berd)'},
        {'kata': 'Fish', 'terjemahan': 'Ikan', 'pelafalan': '(fish)'},
        {'kata': 'Elephant', 'terjemahan': 'Gajah', 'pelafalan': '(elefen)'},
        {'kata': 'Lion', 'terjemahan': 'Singa', 'pelafalan': '(laion)'}
    ],
    # ... (data lain tetap sama seperti sebelumnya)
    "Perasaan": [
        {'kata': 'Happy', 'terjemahan': 'Senang', 'pelafalan': '(hepi)'},
        {'kata': 'Sad', 'terjemahan': 'Sedih', 'pelafalan': '(sed)'},
        {'kata': 'Angry', 'terjemahan': 'Marah', 'pelafalan': '(enggri)'},
        {'kata': 'Scared', 'terjemahan': 'Takut', 'pelafalan': '(skerd)'}
    ]
}

# --- KONFIGURASI TEMA DAN KUSTOMISASI CSS ---

st.set_page_config(
    page_title="Kamus Kosakata Interaktif",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Mengubah warna sidebar */
    .st-emotion-cache-121bd7t.e1ds3rsq1 {
        background-color: #f0f2f6;
        color: #0d47a1;
    }
    .st-emotion-cache-vk3ypu.e1ds3rsq3 {
        color: #0d47a1;
    }
    .st-emotion-cache-1cypj85.e1ds3rsq0 {
        background-color: #ffffff;
    }
    .st-emotion-cache-6q9sum.e1ds3rsq1 {
        background-color: #0d47a1;
        color: white;
        border-radius: 8px;
        border: 1px solid #0d47a1;
    }
    .st-emotion-cache-6q9sum.e1ds3rsq1:hover {
        background-color: #1976d2;
    }
    .st-emotion-cache-14u43f8.e1ds3rsq1 {
        background-color: #1e88e5;
        color: white;
        border-radius: 8px;
        border: 1px solid #1e88e5;
    }
    .st-emotion-cache-14u43f8.e1ds3rsq1:hover {
        background-color: #2196f3;
    }
    .stButton > button {
        background-color: #1e88e5;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 8px 12px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #2196f3;
    }
</style>
""", unsafe_allow_html=True)

# --- ANTARMUKA UTAMA STREAMLIT ---

def main():
    st.title("📚 Kamus Kosakata Inggris-Indonesia")
    st.markdown("""
    <p style="color:#666666;">
    Pilih topik di sidebar untuk melihat daftar kosakata. Klik tombol <span style="color:#1e88e5;">🔊</span> untuk mendengarkan pengucapan.  
    Gunakan 🎙️ untuk mencoba mengucapkan kata dan membandingkannya.
    </p>
    """, unsafe_allow_html=True)

    st.write("---")

    # Sidebar untuk memilih topik
    st.sidebar.title("Pengaturan")
    st.sidebar.title("Pilih Topik")
    topic_list = list(vocab_data.keys())
    selected_topic = st.sidebar.radio("Daftar Topik", topic_list)
    
    st.header(f"Topik: {selected_topic}")
    
    vocabularies = vocab_data.get(selected_topic, [])
    
    for i, vocab in enumerate(vocabularies):
        word = vocab['kata']
        translation = vocab['terjemahan']
        pronunciation = vocab['pelafalan']
        
        col1, col2, col3 = st.columns([0.4, 0.4, 0.2])
        with col1:
            st.markdown(f"**{word}**")
        with col2:
            st.markdown(f"*{translation}* ({pronunciation})")
        with col3:
            if st.button("🔊", key=f"tts_{word}_{i}"):
                audio_file_path = text_to_speech(word)
                with open(audio_file_path, "rb") as f:
                    audio_bytes = f.read()
                    st.audio(audio_bytes, format='audio/mp3', start_time=0)
                os.remove(audio_file_path)

    # --- Fitur Speech to Text ---
    st.write("---")
    st.subheader("🎙️ Uji Pengucapan")
    st.markdown("Klik tombol di bawah untuk mengaktifkan mikrofon lalu ucapkan kosakata:")

    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDONLY,
        audio_processor_factory=AudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )

    if webrtc_ctx.audio_processor:
        recognized_text = webrtc_ctx.audio_processor.text
        if recognized_text:
            st.write(f"🗣️ Anda mengucapkan: **{recognized_text}**")
            vocab_words = [v['kata'].lower() for v in vocabularies]
            if recognized_text.lower() in vocab_words:
                st.success("✅ Pengucapan sesuai dengan salah satu kosakata!")
            else:
                st.error("❌ Belum cocok dengan kosakata yang ada.")

if __name__ == "__main__":
    main()
