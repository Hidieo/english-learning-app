# english.py
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from streamlit_autorefresh import st_autorefresh
import speech_recognition as sr
import av
import threading
import numpy as np
import html

# ==============================
# 1) Data kosakata (sesuaikan)
# ==============================
vocab_data = {
    "Hewan": [
        {"kata": "cat"},
        {"kata": "dog"},
        {"kata": "bird"}
    ],
    "Angka": [
        {"kata": "one"},
        {"kata": "two"},
        {"kata": "three"}
    ]
}
# List kata sederhana (lowercase, tanpa spasi trimming)
vocab_words = [v["kata"].strip().lower() for topic in vocab_data.values() for v in topic]

# ==============================
# 2) Persistent globals (tidak ditimpa pada rerun)
# ==============================
if "TRANSCRIPT" not in globals():
    TRANSCRIPT = []              # akan diisi oleh callback audio
if "TRANSCRIPT_LOCK" not in globals():
    TRANSCRIPT_LOCK = threading.Lock()
if "RECOGNIZER" not in globals():
    RECOGNIZER = sr.Recognizer()

# ==============================
# 3) Audio processing callback
# ==============================
def process_audio(frame: av.AudioFrame):
    """
    Dipanggil oleh streamlit-webrtc pada tiap frame audio.
    Kita konversi Frame -> int16 PCM -> SpeechRecognition AudioData -> transcribe.
    """
    global TRANSCRIPT, TRANSCRIPT_LOCK, RECOGNIZER

    try:
        audio = frame.to_ndarray()  # shape (n_samples, n_channels) atau (n_samples,)
        sample_rate = frame.sample_rate

        # ambil channel pertama kalau stereo
        if audio.ndim > 1:
            audio = audio[:, 0]

        # pastikan int16 PCM
        audio_int16 = audio.astype(np.int16)
        audio_bytes = audio_int16.tobytes()

        # buat AudioData untuk speech_recognition
        audio_data = sr.AudioData(audio_bytes, sample_rate, 2)  # sampwidth=2 (16-bit)

        # Panggil Google free recognizer (bisa gagal jika koneksi/limit)
        try:
            text = RECOGNIZER.recognize_google(audio_data, language="en-US")
            if text and text.strip():
                with TRANSCRIPT_LOCK:
                    TRANSCRIPT.append(text.strip())
        except sr.UnknownValueError:
            # tidak bisa mengenali segmen ini — abaikan
            pass
        except sr.RequestError as e:
            # request error (network/limit) — simpan pesan ringkas untuk debug
            with TRANSCRIPT_LOCK:
                TRANSCRIPT.append(f"[STT ERR]")
    except Exception:
        # tangkap semua error untuk mencegah crash callback
        # jangan tulis detail error ke UI production; cukup ignore
        pass

# ==============================
# 4) UI Streamlit
# ==============================
st.set_page_config(page_title="Live Caption + Vocabulary Highlight", layout="wide")
st.title("🎤 Live Caption (realtime) + Vocabulary Highlight")

st.markdown("Izinkan akses mikrofon ketika browser meminta. Kata yang cocok dengan kosakata akan berwarna hijau.")

# Start WebRTC -> mic (browser) -> server callback process_audio
webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDONLY,
    audio_frame_callback=process_audio,
    media_stream_constraints={"audio": True, "video": False},
)

# area output
output_area = st.empty()

# ==============================
# 5) Auto-refresh setiap 1s supaya UI 'live'
# ==============================
# Pastikan package streamlit-autorefresh sudah di-install (lihat instruksi di bawah)
st_autorefresh(interval=1000, limit=None, key="autosleep")

# ==============================
# 6) Render transcript dengan highlight
# ==============================
with TRANSCRIPT_LOCK:
    last_lines = TRANSCRIPT[-12:]  # ambil 12 terakhir

if not last_lines:
    output_area.markdown("_(Belum ada transkrip — coba bicara setelah izinkan mikrofon di browser.)_")
else:
    html_lines = []
    for line in last_lines:
        words = line.split()
        highlighted = []
        for raw_w in words:
            # keep original display but bandingkan versi "bare" lower
            display_w = html.escape(raw_w)
            bare = "".join(ch for ch in raw_w if ch.isalnum()).lower()
            if bare in vocab_words:
                highlighted.append(f"<span style='color:green; font-weight:700'>{display_w}</span>")
            else:
                highlighted.append(display_w)
        html_lines.append(" ".join(highlighted))
    output_area.markdown("<br>".join(html_lines), unsafe_allow_html=True)
