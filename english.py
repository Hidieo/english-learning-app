"""
Full Streamlit app: Kamus Kosakata Inggris-Indonesia (Final)
Features:
- TTS (gTTS) per vocabulary (playback)
- Browser-based STT using streamlit-webrtc
- Auto-check empty buffer (safe for Streamlit Cloud)
- ICE servers config (STUN + TURN) for better WebRTC connection
- If recognized text matches the vocabulary -> shows ✅

Notes & deployment instructions (below) — keep this file in your GitHub repo as `app.py`.

REQUIREMENTS (requirements.txt):
streamlit
streamlit-webrtc==0.50.0
gtts
speechrecognition
av
numpy
pydub

DEPLOY TO STREAMLIT CLOUD:
1. Push this file as `app.py` and `requirements.txt` to GitHub.
2. Go to https://share.streamlit.io → "New app" → select repo → deploy.
3. Allow microphone in the browser when asked.

"""

import streamlit as st
from gtts import gTTS
import os
import threading
import numpy as np
import av
import io
import wave

from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import speech_recognition as sr

# ----------------- CONFIG -----------------
TEMP_AUDIO_DIR = "temp_audio"
if not os.path.exists(TEMP_AUDIO_DIR):
    os.makedirs(TEMP_AUDIO_DIR)

st.set_page_config(page_title="Kamus Kosakata Interaktif", page_icon="📚", layout="centered")

# ----------------- DATA -----------------
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
    ],
}

# ----------------- HELPERS -----------------
def text_to_speech(text: str) -> str:
    """Generate TTS MP3 and return path"""
    safe_name = text.replace(' ', '_')
    out_path = os.path.join(TEMP_AUDIO_DIR, f"{safe_name}.mp3")
    if not os.path.exists(out_path):
        tts = gTTS(text=text, lang='en')
        tts.save(out_path)
    return out_path


def frames_to_wav_bytes(frames):
    """Convert av.AudioFrame list into WAV bytes (int16 mono)"""
    if not frames:
        return None
    sample_rate = frames[0].sample_rate
    pcm_arrays = []
    for frame in frames:
        arr = frame.to_ndarray()
        if arr.ndim == 2:  # stereo → mono
            arr = arr.mean(axis=0)
        pcm_arrays.append(arr)
    concat = np.concatenate(pcm_arrays).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(concat.tobytes())
    buf.seek(0)
    return buf.read()

# ----------------- AUDIO PROCESSOR -----------------
class RecorderProcessor(AudioProcessorBase):
    def __init__(self):
        self._frames = []
        self._lock = threading.Lock()

    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        with self._lock:
            self._frames.append(frame)
            if len(self._frames) > 200:  # limit buffer
                self._frames = self._frames[-200:]
        return frame

    def get_and_clear_recording(self):
        with self._lock:
            frames = list(self._frames)
            self._frames = []
        return frames

# ----------------- UI -----------------
st.title("📚 Kamus Kosakata Inggris-Indonesia — Final Version")
st.markdown("Pilih topik dari sidebar. Klik 🔊 untuk mendengar pengucapan; klik 🎙️ untuk merekam pengucapan Anda.")

# Sidebar
topic_list = list(vocab_data.keys())
selected_topic = st.sidebar.radio("Daftar Topik", topic_list)

# WebRTC init (once, global)
webrtc_ctx = webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDRECV,
    audio_processor_factory=RecorderProcessor,
    media_stream_constraints={"audio": True, "video": False},
    rtc_configuration={  # ✅ ICE servers
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]},
            {
                "urls": ["turn:openrelay.metered.ca:80", "turn:openrelay.metered.ca:443"],
                "username": "openrelayproject",
                "credential": "openrelayproject",
            },
        ]
    },
)

# Render vocab
vocabularies = vocab_data.get(selected_topic, [])
for i, vocab in enumerate(vocabularies):
    word = vocab['kata']
    translation = vocab['terjemahan']
    pronunciation = vocab['pelafalan']

    col1, col2, col3 = st.columns([0.4, 0.4, 0.2])
    with col1:
        st.markdown(f"**{word}**")
    with col2:
        st.markdown(f"*{translation}* {pronunciation}")
    with col3:
        # 🔊 TTS
        if st.button("🔊", key=f"tts_{selected_topic}_{i}"):
            path = text_to_speech(word)
            st.audio(path)

        # 🎙️ STT
        if st.button("🎙️", key=f"stt_{selected_topic}_{i}"):
            if webrtc_ctx and webrtc_ctx.state.playing and webrtc_ctx.audio_processor:
                frames = webrtc_ctx.audio_processor.get_and_clear_recording()
                wav_bytes = frames_to_wav_bytes(frames)
                if wav_bytes is None:
                    st.warning("⚠️ Tidak ada audio — coba tekan 🎙️ lagi dan ucapkan 1-3 detik.")
                else:
                    recognizer = sr.Recognizer()
                    with sr.AudioFile(io.BytesIO(wav_bytes)) as source:
                        audio_data = recognizer.record(source)
                    try:
                        recognized = recognizer.recognize_google(audio_data, language='en-US')

                        def normalize(s): return ''.join(ch for ch in s.lower() if ch.isalnum() or ch.isspace()).strip()
                        if normalize(recognized) == normalize(word):
                            st.success(f"✅ Cocok! Anda mengucapkan: **{recognized}**")
                        else:
                            st.error(f"❌ Tidak cocok. Anda mengucapkan: **{recognized}**")
                            st.info(f"Target: **{word}**")
                    except sr.UnknownValueError:
                        st.warning("⚠️ Tidak bisa mengenali audio.")
                    except sr.RequestError as e:
                        st.error(f"⚠️ Gagal koneksi ke Speech API: {e}")
            else:
                st.warning("⚠️ Microphone belum aktif atau WebRTC belum siap.")

st.markdown("---")
st.caption("STT menggunakan Google Web Speech API (SpeechRecognition). Hasil tergantung jaringan dan kualitas rekaman.")
