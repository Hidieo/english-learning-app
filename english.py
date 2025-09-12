"""
Full Streamlit app: Kamus Kosakata Inggris-Indonesia (Stable WebRTC + retries)

Notes:
- Tambahkan requirements.txt:
    streamlit
    streamlit-webrtc==0.50.0
    gtts
    speechrecognition
    av
    numpy
    pydub

- Deploy to share.streamlit.io OR run locally with:
    streamlit run app.py

- Pastikan browser mengizinkan microphone. Setelah klik "Start" tunggu 2-3 detik sebelum menekan tombol 🎙️.
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
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase

# ----------------- CONFIG -----------------
TEMP_AUDIO_DIR = "temp_audio"
if not os.path.exists(TEMP_AUDIO_DIR):
    os.makedirs(TEMP_AUDIO_DIR)

st.set_page_config(page_title="Kamus Kosakata Interaktif", page_icon="📚", layout="wide")

# ----------------- DATA (singkat / contoh) -----------------
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
    """Generate TTS MP3 and return path (cached)."""
    safe_name = text.replace(' ', '_')
    out_path = os.path.join(TEMP_AUDIO_DIR, f"{safe_name}.mp3")
    if not os.path.exists(out_path):
        tts = gTTS(text=text, lang='en')
        tts.save(out_path)
    return out_path


def frames_to_wav_bytes(frames):
    """Convert a list of av.AudioFrame into WAV bytes (int16 mono)."""
    if not frames:
        return None
    sample_rate = frames[0].sample_rate
    pcm_arrays = []
    for frame in frames:
        arr = frame.to_ndarray()
        # arr shape: (channels, samples) or (samples,) depending on conversion
        if arr.ndim == 2:
            # average channels -> mono
            arr = arr.mean(axis=0)
        pcm_arrays.append(arr)
    concat = np.concatenate(pcm_arrays).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(concat.tobytes())
    buf.seek(0)
    return buf.read()


# ----------------- AUDIO PROCESSOR -----------------
class RecorderProcessor(AudioProcessorBase):
    """Saves recent audio frames to an internal buffer (thread-safe)."""
    def __init__(self):
        self._frames = []
        self._lock = threading.Lock()

    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        # Debug: print frame info to Streamlit logs (lihat logs di Streamlit Cloud)
        try:
            arr = frame.to_ndarray()
            # Print minimal info for debugging
            print(f"[recv_audio] frame rate={frame.sample_rate} dtype={arr.dtype} shape={arr.shape}")
        except Exception as e:
            print(f"[recv_audio] frame to_ndarray error: {e}")

        with self._lock:
            self._frames.append(frame)
            # keep last N frames to limit memory (approx few seconds)
            if len(self._frames) > 250:
                self._frames = self._frames[-250:]
        return frame

    def get_and_clear_recording(self):
        with self._lock:
            frames = list(self._frames)
            self._frames = []
        return frames


# ----------------- UI LAYOUT -----------------
st.title("📚 Kamus Kosakata Inggris-Indonesia — WebRTC STT (Improved)")
st.write("Instruksi: Klik **Start** (panel WebRTC di sidebar), tunggu 2-3 detik, lalu tekan tombol 🎙️ di kata yang ingin direkam.")

# Sidebar: topics + WebRTC control
st.sidebar.title("Pengaturan & STT (Mic)")
topic_list = list(vocab_data.keys())
selected_topic = st.sidebar.radio("Daftar Topik", topic_list)

st.sidebar.markdown("---")
st.sidebar.markdown("**Kontrol WebRTC / Microphone**")
st.sidebar.markdown("1) Klik *Start* pada widget WebRTC di bawah → izinkan microphone di browser.  \n2) Tunggu 2-3 detik agar buffer terisi.  \n3) Kembali ke halaman utama, lalu tekan 🎙️ pada kosakata yang ingin diuji.")

# ----------------- WebRTC START (global) -----------------
# media_stream_constraints: lebih eksplisit untuk performa lebih baik
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
    rtc_configuration={  # ICE servers: STUN + TURN (openrelay as public TURN)
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]},
            {
                "urls": ["turn:openrelay.metered.ca:80", "turn:openrelay.metered.ca:443"],
                "username": "openrelayproject",
                "credential": "openrelayproject",
            },
        ]
    },
    async_processing=True,
    audio_receiver_size=256,
    auto_play_audio=True
)

# Show the webrtc status / small hint
if webrtc_ctx.state.playing:
    st.sidebar.success("WebRTC: microphone aktif ✅")
else:
    st.sidebar.info("WebRTC: Tekan 'Start' dan izinkan microphone di browser.")

st.sidebar.caption("Jika WebRTC tidak berhasil, cek logs di Streamlit Cloud untuk 'Frame' debug info.")

# ----------------- MAIN: render vocab rows -----------------
st.header(f"Topik: {selected_topic}")
st.markdown("Klik 🔊 untuk mendengar kata. Klik 🎙️ untuk merekam dan memeriksa apakah pengucapanmu cocok.")

vocabularies = vocab_data.get(selected_topic, [])

# Helper normalize for comparison
def normalize_text(s: str) -> str:
    return ''.join(ch for ch in s.lower() if ch.isalnum() or ch.isspace()).strip()

# For each vocab row
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
        # TTS button
        if st.button("🔊", key=f"tts_{selected_topic}_{i}"):
            path = text_to_speech(word)
            st.audio(path)

        # STT button
        if st.button("🎙️", key=f"stt_{selected_topic}_{i}"):
            # Quick guard: ensure webrtc running and processor exists
            if not (webrtc_ctx and webrtc_ctx.state.playing and webrtc_ctx.audio_processor):
                st.warning("⚠️ WebRTC belum aktif / microphone belum diizinkan. Pastikan klik Start dan izinkan microphone di browser.")
            else:
                processor = webrtc_ctx.audio_processor

                # Try multiple times to fetch frames (simple retry), because sometimes immediatelly after Start frames kosong.
                frames = None
                attempts = 3
                for attempt in range(attempts):
                    frames = processor.get_and_clear_recording()
                    if frames:
                        break
                    # if not frames, wait a bit and try again
                    time.sleep(0.6)
                wav_bytes = frames_to_wav_bytes(frames)

                if wav_bytes is None:
                    st.warning("⚠️ Tidak ada audio yang direkam — coba tekan 🎙️ lagi dan ucapkan selama 1-3 detik. Pastikan juga microphone diizinkan dan tunggu beberapa detik setelah klik Start.")
                else:
                    # Play back the recorded audio for user feedback
                    st.audio(wav_bytes, format="audio/wav")

                    # Use SpeechRecognition to transcribe
                    recognizer = sr.Recognizer()
                    try:
                        with sr.AudioFile(io.BytesIO(wav_bytes)) as source:
                            audio_data = recognizer.record(source)
                        recognized = recognizer.recognize_google(audio_data, language='en-US')

                        # Normalize and compare
                        if normalize_text(recognized) == normalize_text(word):
                            st.success(f"✅ Cocok! Anda mengucapkan: **{recognized}**")
                        else:
                            st.error(f"❌ Tidak cocok. Anda mengucapkan: **{recognized}**")
                            st.info(f"Target: **{word}**")
                            # Also show similarity score (optional)
                            from difflib import SequenceMatcher
                            score = SequenceMatcher(None, normalize_text(recognized), normalize_text(word)).ratio() * 100
                            st.caption(f"Similarity: {score:.1f}%")

                    except sr.UnknownValueError:
                        st.warning("⚠️ Google Speech Recognition tidak dapat mengenali audio — coba ulangi dengan suara lebih jelas.")
                    except sr.RequestError as e:
                        st.error(f"⚠️ Gagal terhubung ke layanan pengenalan suara: {e}")
                    except Exception as e:
                        st.error(f"⚠️ Error saat memproses audio: {e}")

st.markdown("---")
st.caption("Catatan: Jika WebRTC tidak bekerja pada jaringan tertentu, pertimbangkan fallback: upload file audio (record di ponsel/PC lalu upload) atau gunakan layanan STT pihak ketiga (Whisper/Google Cloud). Lihat logs Streamlit (Manage app -> Logs) untuk debug frame info.")

# Optional: cleanup TTS cache
if st.sidebar.button("Bersihkan cache TTS"):
    removed = 0
    for f in os.listdir(TEMP_AUDIO_DIR):
        p = os.path.join(TEMP_AUDIO_DIR, f)
        try:
            os.remove(p)
            removed += 1
        except Exception:
            pass
    st.sidebar.success(f"Cache dibersihkan ({removed} file).")
