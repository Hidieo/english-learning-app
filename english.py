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

TEMP_AUDIO_DIR = "temp_audio"
if not os.path.exists(TEMP_AUDIO_DIR):
    os.makedirs(TEMP_AUDIO_DIR)

st.set_page_config(page_title="Kamus Kosakata Interaktif", page_icon="📚", layout="centered")

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
        {'kata': 'Grape', 'terjemahan': 'Anggur', 'pelafalan': '(grep)'},
        {'kata': 'Mango', 'terjemahan': 'Mangga', 'pelafalan': '(menggo)'}
    ]
}

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
        arr = arr.astype(np.int16)
        pcm_arrays.append(arr)
    concat = np.concatenate(pcm_arrays)
    int16 = concat.astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int16.tobytes())
    buf.seek(0)
    return buf.read()

class RecorderProcessor(AudioProcessorBase):
    def __init__(self):
        self._frames = []
        self._lock = threading.Lock()

    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        with self._lock:
            self._frames.append(frame)
            if len(self._frames) > 200:
                self._frames = self._frames[-200:]
        return frame

    def get_and_clear_recording(self):
        with self._lock:
            frames = list(self._frames)
            self._frames = []
        return frames

st.title("📚 Kamus Kosakata Inggris-Indonesia — Full Version")
st.markdown("Pilih topik dari sidebar. Klik 🔊 untuk mendengar pengucapan; klik 🎙️ untuk merekam pengucapan Anda. Jika cocok dengan kosakata, akan muncul ✅.")

st.sidebar.title("Pengaturan")
topic_list = list(vocab_data.keys())
selected_topic = st.sidebar.radio("Daftar Topik", topic_list)

st.header(f"Topik: {selected_topic}")

st.sidebar.markdown("---")
st.sidebar.markdown("**STT (microphone)**")

webrtc_ctx = webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDRECV,
    audio_processor_factory=RecorderProcessor,
    audio_receiver_size=256,
    media_stream_constraints={"audio": True, "video": False},
)

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
        tts_key = f"tts_{selected_topic}_{i}"
        if st.button("🔊", key=tts_key):
            path = text_to_speech(word)
            st.audio(path)

        stt_key = f"stt_{selected_topic}_{i}"
        if st.button("🎙️", key=stt_key):
            if webrtc_ctx and webrtc_ctx.state.playing and webrtc_ctx.audio_processor:
                processor = webrtc_ctx.audio_processor
                frames = processor.get_and_clear_recording()

                if not frames:
                    st.warning("⚠️ Tidak ada audio yang terekam. Coba ulangi dengan suara lebih jelas.")
                else:
                    wav_bytes = frames_to_wav_bytes(frames)
                    if wav_bytes is None:
                        st.warning("⚠️ Rekaman kosong — coba tekan tombol 🎙️ lagi sambil mengucapkan kata.")
                    else:
                        recognizer = sr.Recognizer()
                        with sr.AudioFile(io.BytesIO(wav_bytes)) as source:
                            audio_data = recognizer.record(source)
                        try:
                            recognized = recognizer.recognize_google(audio_data, language="en-US")

                            def normalize(s):
                                return "".join(ch for ch in s.lower() if ch.isalnum() or ch.isspace()).strip()

                            if normalize(recognized) == normalize(word):
                                st.success(f"✅ Cocok! Anda mengucapkan: **{recognized}**")
                            else:
                                st.error(f"❌ Tidak cocok. Anda mengucapkan: **{recognized}**")
                                st.info(f"Target: **{word}**")

                        except sr.UnknownValueError:
                            st.warning("⚠️ Suara tidak dapat dikenali, coba ulangi.")
                        except sr.RequestError as e:
                            st.error(f"⚠️ Gagal menghubungi layanan STT: {e}")
            else:
                st.warning("⚠️ Microphone belum aktif. Pastikan izin mic sudah diberikan.")

st.markdown("---")
st.caption("Catatan: STT menggunakan Google Web Speech API lewat library SpeechRecognition.")

if st.sidebar.button('Bersihkan TTS cache'):
    files = os.listdir(TEMP_AUDIO_DIR)
    for f in files:
        try:
            os.remove(os.path.join(TEMP_AUDIO_DIR, f))
        except Exception:
            pass
    st.sidebar.success('Cache dibersihkan')
