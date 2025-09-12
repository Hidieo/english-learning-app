# -*- coding: utf-8 -*-
import streamlit as st
import gtts
from gtts import gTTS
import os
import tempfile
from st_audiorec import st_audiorec
import speech_recognition as sr

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
    # ... (lanjutkan semua data kosakata Anda di sini)
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
    /* Sidebar */
    .st-emotion-cache-121bd7t.e1ds3rsq1 {
        background-color: #f0f2f6;
        color: #0d47a1;
    }
    .st-emotion-cache-vk3ypu.e1ds3rsq3 {
        color: #0d47a1;
    }
    /* Background */
    .st-emotion-cache-1cypj85.e1ds3rsq0 {
        background-color: #ffffff;
    }
    /* Button */
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
    </p>
    """, unsafe_allow_html=True)

    st.write("---")

    # Sidebar
    st.sidebar.title("Pengaturan")
    theme_option = st.sidebar.radio(
        "Pilih Tema Latar Belakang",
        ("Terang (Biru & Putih)", "Gelap (Default)")
    )

    st.sidebar.markdown("---")
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

    # --- FITUR SPEECH-TO-TEXT ---
    st.write("---")
    st.header("🎙️ Coba Speech-to-Text")

    wav_audio_data = st_audiorec()

    if wav_audio_data is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            tmpfile.write(wav_audio_data)
            tmpfile_path = tmpfile.name

        recognizer = sr.Recognizer()
        with sr.AudioFile(tmpfile_path) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio, language="en-US")
                st.success(f"Terdeteksi: {text}")
            except sr.UnknownValueError:
                st.warning("❌ Suara tidak bisa dikenali")
            except sr.RequestError:
                st.error("⚠️ Gagal terhubung ke Google Speech API")


if __name__ == "__main__":
    main()
