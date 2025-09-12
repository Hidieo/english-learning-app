"""
Full Streamlit app: Kamus Kosakata Inggris-Indonesia (Stable WebRTC + retries + waveform live)

Requirements:
    streamlit
    streamlit-webrtc==0.50.0
    gtts
    speechrecognition
    av
    numpy
    pydub
    matplotlib
"""

import streamlit as st
from gtts import gTTS
import os
import threading
import numpy as np
import av
import io
import wave
import time
import speech_recognition as sr
import matplotlib.pyplot as plt
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase

# ----------------- CONFIG -----------------
TEMP_AUDIO_DIR = "temp_audio"
if not os.path.exists(TEMP_AUDIO_DIR):
    os.makedirs(TEMP_AUDIO_DIR)

st.set_page_config(page_title="Kamus Kosakata Interaktif", page_icon="📚", layout="wide")

# ----------------- DATA -----------------
vocab_data = {
    "Hewan": [
        {'kata': 'Cat', 'terjemahan': 'Kucing', 'pelafalan': '(ket)'},
        {'kata': 'Dog', 'terjemahan': 'Anjing', 'pelafalan': '(dog)'},
        {'kata': 'Bird', 'terjemahan': 'Burung', 'pelafalan': '(berd)'},
        {'kata': 'Fish', 'terjemahan': 'Ikan', 'pelafalan': '(fish)'},
        {'kata': 'Elephant', 'terjemahan': 'Gajah', 'pelafalan': '(elefen)'},
        {'kata': 'Lion', 'terjemahan': 'Singa', 'pelafalan': '(laion)'}
    ],
    "Buah-buahan": [
        {'kata': 'Apple', 'terjemahan': 'Apel', 'pelafalan': '(epel)'},
        {'kata': 'Banana', 'terjemahan': 'Pisang', 'pelafalan': '(bænana)'},
        {'kata': 'Orange', 'terjemahan': 'Jeruk', 'pelafalan': '(orej)'},
    ],
}

# ----------------- HELPERS -----------------
def text_to_speech(text: str) -> str:
    safe_name = text.replace(' ', '_')
    out_path = os.path.join(TEMP_AUDIO_DIR, f"{safe_name}.mp3")
    if not os.path.exists(out_path):
        tts = gTTS(text=text, lang='en')
        tts.save(out_path)
    return out_path


def frames_to_wav_bytes(frames):
    if not frames:
        return None
    sample_rate = frames[0].sample_rate
    pcm_arrays = []
    for frame in frames:
        arr = frame.to_ndarray()
        if arr.ndim == 2:
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
        self.waveform = np.zeros(100)

    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        arr = frame.to_ndarray()
        if arr.ndim == 2:
            arr = arr[:, 0]

        # update waveform (last 100 samples RMS-based)
        rms = np.sqrt(np.mean(arr.astype(np.float32) ** 2))
        self.waveform = np.roll(self.waveform, -1)
        self.waveform[-1] = rms

        with self._lock:
            self._frames.append(frame)
            if len(self._frames) > 250:
                self._frames = self._frames[-250:]
        return frame

    def get_and_clear_recording(self):
        with self._lock:
            frames = list(self._frames)
            self._frames = []
        return frames


# ----------------- UI -----------------
st.title("📚 Kamus Kosakata Inggris-Indonesia — WebRTC STT (Waveform)")
st.write("Instruksi: Klik **Start** (panel WebRTC di sidebar), tunggu 2-3 detik, lalu tekan tombol 🎙️ di kata yang ingin direkam.")

# Sidebar
st.sidebar.title("Pengaturan & STT (Mic)")
topic_list = list(vocab_data.keys())
selected_topic = st.sidebar.radio("Daftar Topik", topic_list)

st.sidebar.markdown("---")
st.sidebar.markdown("**Kontrol WebRTC / Microphone**")
st.sidebar.markdown("1) Klik *Start* pada widget WebRTC di bawah → izinkan microphone.  \n2) Tunggu 2-3 detik agar buffer terisi.  \n3) Tekan 🎙️ di kata.")

media_constraints = {
    "audio": {
        "echoCancellation": True,
        "noiseSuppression": True,
        "autoGainControl": True,
    },
    "video": False,
}

webrtc_ctx = webrtc_streamer(
    key="speech-to-text-global",
    mode=WebRtcMode.SENDRECV,
    audio_processor_factory=RecorderProcessor,
    media_stream_constraints=media_constraints,
    rtc_configuration={
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]},
            {"urls": ["turn:openrelay.metered.ca:80", "turn:openrelay.metered.ca:443"],
             "username": "openrelayproject", "credential": "openrelayproject"}
        ]
    },
    async_processing=True,
    audio_receiver_size=256
)

# Waveform live indikator
if webrtc_ctx and webrtc_ctx.state.playing and webrtc_ctx.audio_processor:
    proc = webrtc_ctx.audio_processor
    wf_placeholder = st.sidebar.empty()

    def plot_waveform(waveform):
        fig, ax = plt.subplots(figsize=(3,1))
        ax.plot(waveform, color="cyan")
        ax.set_ylim(0, np.max(waveform)*1.2 + 1e-3)
        ax.axis("off")
        return fig

    wf_placeholder.pyplot(plot_waveform(proc.waveform))

# Status
if webrtc_ctx.state.playing:
    st.sidebar.success("WebRTC: microphone aktif ✅")
else:
    st.sidebar.info("WebRTC: Tekan 'Start' dan izinkan microphone.")

# ----------------- MAIN -----------------
st.header(f"Topik: {selected_topic}")
st.markdown("Klik 🔊 untuk mendengar kata. Klik 🎙️ untuk merekam & cek pengucapan.")

vocabularies = vocab_data.get(selected_topic, [])

def normalize_text(s: str) -> str:
    return ''.join(ch for ch in s.lower() if ch.isalnum() or ch.isspace()).strip()

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
        if st.button("🔊", key=f"tts_{selected_topic}_{i}"):
            path = text_to_speech(word)
            st.audio(path)

        if st.button("🎙️", key=f"stt_{selected_topic}_{i}"):
            if not (webrtc_ctx and webrtc_ctx.state.playing and webrtc_ctx.audio_processor):
                st.warning("⚠️ WebRTC belum aktif / mic belum diizinkan.")
            else:
                processor = webrtc_ctx.audio_processor
                frames = None
                for _ in range(3):  # retry sampai 3x
                    frames = processor.get_and_clear_recording()
                    if frames:
                        break
                    time.sleep(0.6)

                wav_bytes = frames_to_wav_bytes(frames)
                if wav_bytes is None:
                    st.warning("⚠️ Tidak ada audio — ulangi dan bicara lebih jelas 1–3 detik.")
                else:
                    st.audio(wav_bytes, format="audio/wav")
                    recognizer = sr.Recognizer()
                    try:
                        with sr.AudioFile(io.BytesIO(wav_bytes)) as source:
                            audio_data = recognizer.record(source)
                        recognized = recognizer.recognize_google(audio_data, language='en-US')
                        if normalize_text(recognized) == normalize_text(word):
                            st.success(f"✅ Cocok! Anda mengucapkan: **{recognized}**")
                        else:
                            st.error(f"❌ Tidak cocok. Anda mengucapkan: **{recognized}**")
                            st.info(f"Target: **{word}**")
                            from difflib import SequenceMatcher
                            score = SequenceMatcher(None, normalize_text(recognized), normalize_text(word)).ratio() * 100
                            st.caption(f"Similarity: {score:.1f}%")
                    except sr.UnknownValueError:
                        st.warning("⚠️ Google tidak bisa mengenali audio.")
                    except Exception as e:
                        st.error(f"⚠️ Error: {e}")
