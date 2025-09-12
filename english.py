import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from streamlit_autorefresh import st_autorefresh
import speech_recognition as sr
import av
import threading
import numpy as np

# ==============================
# 1. Data kosakata
# ==============================
vocab_data = {
    "Greeting And Introduction": [
        {"kata": "hello"},
        {"kata": "good morning"},
        {"kata": "how are you"}
    ],
    "Numbers, Dates, And Time": [
        {"kata": "one"},
        {"kata": "two"},
        {"kata": "three"}
    ]
}

vocab_words = [v["kata"].lower() for topic in vocab_data.values() for v in topic]

# ==============================
# 2. Variabel global
# ==============================
transcript = []
recognizer = sr.Recognizer()
lock = threading.Lock()

# ==============================
# 3. Audio processing callback
# ==============================
def process_audio(frame: av.AudioFrame):
    audio = frame.to_ndarray()
    sample_rate = frame.sample_rate

    # Ambil channel pertama kalau stereo
    if audio.ndim > 1:
        audio = audio[:, 0]

    # Convert ke PCM 16-bit
    audio_bytes = audio.astype(np.int16).tobytes()
    audio_data = sr.AudioData(audio_bytes, sample_rate, 2)

    try:
        text = recognizer.recognize_google(audio_data, language="en-US")
        with lock:
            transcript.append(text)
    except sr.UnknownValueError:
        pass

# ==============================
# 4. UI Streamlit
# ==============================
st.title("🎤 Live Caption + Vocabulary Highlight")

webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDONLY,   # ✅ enum, bukan string
    audio_frame_callback=process_audio,
    media_stream_constraints={"audio": True, "video": False},
)

# Tempat menampilkan hasil transkrip
output_area = st.empty()

# ==============================
# 5. Render transcript dengan highlight
# ==============================
def render_transcript():
    with lock:
        displayed_text = []
        for text in transcript[-10:]:  # tampilkan 10 terakhir
            words = text.split()
            highlighted = []
            for w in words:
                if w.lower() in vocab_words:
                    highlighted.append(
                        f"<span style='color:lime;font-weight:bold'>{w}</span>"
                    )
                else:
                    highlighted.append(w)
            displayed_text.append(" ".join(highlighted))

        if displayed_text:
            output_area.markdown("<br>".join(displayed_text), unsafe_allow_html=True)

# Auto-refresh tiap 1 detik
st_autorefresh(interval=1000, limit=None, key="refresh")

render_transcript()
