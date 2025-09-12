# -*- coding: utf-8 -*-
import streamlit as st
import gtts
from gtts import gTTS
import os
import speech_recognition as sr
from difflib import SequenceMatcher

# ------------------------------
# Setup direktori audio
# ------------------------------
TEMP_AUDIO_DIR = "temp_audio"
if not os.path.exists(TEMP_AUDIO_DIR):
    os.makedirs(TEMP_AUDIO_DIR)

# ------------------------------
# Fungsi TTS
# ------------------------------
def text_to_speech(text):
    """Mengubah teks menjadi file audio MP3."""
    tts = gTTS(text=text, lang='en')
    with open(f"{TEMP_AUDIO_DIR}/temp.mp3", "wb") as f:
        tts.write_to_fp(f)
    return f"{TEMP_AUDIO_DIR}/temp.mp3"

# ------------------------------
# Fungsi STT dan Evaluasi
# ------------------------------
def get_similarity(a: str, b: str) -> float:
    """Return similarity ratio (0-1) between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def recognize_speech(timeout: int = 5, phrase_time_limit: int = 7) -> str:
    """Capture audio from microphone and return recognized text (Google API)."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... please speak the word.")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    return r.recognize_google(audio)

def evaluate_pronunciation(target: str, recognized: str) -> dict:
    """Evaluate pronunciation similarity and return results as dict."""
    score = get_similarity(target, recognized) * 100
    if score > 85:
        feedback = "✅ Excellent pronunciation!"
    elif score > 60:
        feedback = "👍 Good, but can be improved."
    else:
        feedback = "⚠️ Needs practice. Try speaking more clearly."
    return {"recognized": recognized, "score": score, "feedback": feedback}

# ------------------------------
# Data Kosakata
# ------------------------------
vocab_data = {
    "Hewan": [
        {'kata': 'Cat', 'terjemahan': 'Kucing', 'pelafalan': '(ket)'},
        {'kata': 'Dog', 'terjemahan': 'Anjing', 'pelafalan': '(dog)'},
        {'kata': 'Bird', 'terjemahan': 'Burung', 'pelafalan': '(berd)'},
        {'kata': 'Fish', 'terjemahan': 'Ikan', 'pelafalan': '(fish)'},
        {'kata': 'Elephant', 'terjemahan': 'Gajah', 'pelafalan': '(elefen)'},
    ]
}

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(
    page_title="Kamus Kosakata Interaktif",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

def main():
    st.title("📚 Kamus Kosakata Inggris-Indonesia")
    st.write("Klik tombol 🔊 untuk mendengar pengucapan, lalu coba ucapkan dengan 🎙️.")

    topic_list = list(vocab_data.keys())
    selected_topic = st.sidebar.radio("Daftar Topik", topic_list)
    st.header(f"Topik: {selected_topic}")

    vocabularies = vocab_data.get(selected_topic, [])

    for i, vocab in enumerate(vocabularies):
        word = vocab['kata']
        translation = vocab['terjemahan']
        pronunciation = vocab['pelafalan']

        col1, col2, col3, col4 = st.columns([0.3, 0.3, 0.2, 0.2])

        with col1:
            st.markdown(f"**{word}**")
        with col2:
            st.markdown(f"*{translation}* {pronunciation}")

        # Tombol TTS
        with col3:
            if st.button("🔊", key=f"tts_{word}_{i}"):
                audio_file_path = text_to_speech(word)
                with open(audio_file_path, "rb") as f:
                    audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3")
                os.remove(audio_file_path)

        # Tombol STT
        with col4:
            if st.button("🎙️", key=f"stt_{word}_{i}"):
                try:
                    recognized = recognize_speech()
                    result = evaluate_pronunciation(word, recognized)

                    if result["score"] > 85:
                        st.success(f"✅ Cocok! Kamu mengucapkan: {result['recognized']}")
                    else:
                        st.warning(f"❌ Kamu mengucapkan: {result['recognized']}\n\n{result['feedback']}")

                except sr.UnknownValueError:
                    st.error("😕 Maaf, tidak bisa mengenali ucapan kamu.")
                except sr.RequestError as e:
                    st.error(f"API error: {e}")

if __name__ == "__main__":
    main()
