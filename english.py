"""
Full Streamlit app: Kamus Kosakata Inggris-Indonesia
Features:
- TTS (gTTS) per vocabulary (playback)
- Browser-based STT using streamlit-webrtc
- When user records and the recognized text matches the vocabulary -> shows green check ✅

Notes & deployment instructions (below) — keep this file in your GitHub repo as `app.py`.

REQUIREMENTS (requirements.txt):
streamlit
streamlit-webrtc==0.50.0
gtts
speechrecognition
av
numpy
pydub

(Depending on hosting, some packages like `av` and `pydub` may be preinstalled or require binary wheels.)

DEPLOY TO STREAMLIT CLOUD (share.streamlit.io):
1. Create a new GitHub repo and push this file as `app.py`.
2. Add a file `requirements.txt` containing the lines above.
3. Go to https://share.streamlit.io and click "New app" — choose the repo, branch, and `app.py`.
4. Grant permissions and deploy. The app will run in the browser and can access the user's microphone via WebRTC.

USAGE NOTES:
- The STT uses `streamlit-webrtc` to receive short audio segments from the browser, converts them to WAV, then uses `speech_recognition` (Google Web Speech API) to transcribe.
- Transcription accuracy depends on network and Google's speech service; short single words generally transcribe well.
- If you encounter issues with `av` on Streamlit Cloud, check the deployment logs to see if any binary wheels are missing.

"""

import streamlit as st
from gtts import gTTS
import os
import tempfile
import time
import threading
import queue
import numpy as np
import av
import io
import contextlib
import wave
import base64

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
    ],
    "Warna": [
        {'kata': 'Red', 'terjemahan': 'Merah', 'pelafalan': '(red)'},
        {'kata': 'Blue', 'terjemahan': 'Biru', 'pelafalan': '(blu)'},
        {'kata': 'Green', 'terjemahan': 'Hijau', 'pelafalan': '(grin)'},
        {'kata': 'Yellow', 'terjemahan': 'Kuning', 'pelafalan': '(yelo)'},
        {'kata': 'Black', 'terjemahan': 'Hitam', 'pelafalan': '(blek)'}
    ],
    "Angka": [
        {'kata': 'One', 'terjemahan': 'Satu', 'pelafalan': '(wan)'},
        {'kata': 'Two', 'terjemahan': 'Dua', 'pelafalan': '(tu)'},
        {'kata': 'Three', 'terjemahan': 'Tiga', 'pelafalan': '(tri)'},
        {'kata': 'Four', 'terjemahan': 'Empat', 'pelafalan': '(for)'},
        {'kata': 'Five', 'terjemahan': 'Lima', 'pelafalan': '(faiv)'}
    ],
    "Bagian Tubuh": [
        {'kata': 'Head', 'terjemahan': 'Kepala', 'pelafalan': '(hed)'},
        {'kata': 'Hand', 'terjemahan': 'Tangan', 'pelafalan': '(hend)'},
        {'kata': 'Foot', 'terjemahan': 'Kaki', 'pelafalan': '(fut)'},
        {'kata': 'Eye', 'terjemahan': 'Mata', 'pelafalan': '(ai)'},
        {'kata': 'Ear', 'terjemahan': 'Telinga', 'pelafalan': '(ir)'}
    ],
    "Transportasi": [
        {'kata': 'Car', 'terjemahan': 'Mobil', 'pelafalan': '(kar)'},
        {'kata': 'Bus', 'terjemahan': 'Bus', 'pelafalan': '(bas)'},
        {'kata': 'Train', 'terjemahan': 'Kereta', 'pelafalan': '(tren)'},
        {'kata': 'Bicycle', 'terjemahan': 'Sepeda', 'pelafalan': '(baisikel)'},
        {'kata': 'Airplane', 'terjemahan': 'Pesawat', 'pelafalan': '(erplen)'}
    ],
    "Pakaian": [
        {'kata': 'Shirt', 'terjemahan': 'Kemeja', 'pelafalan': '(syert)'},
        {'kata': 'Pants', 'terjemahan': 'Celana', 'pelafalan': '(pents)'},
        {'kata': 'Dress', 'terjemahan': 'Gaun', 'pelafalan': '(dres)'},
        {'kata': 'Shoes', 'terjemahan': 'Sepatu', 'pelafalan': '(syus)'},
        {'kata': 'Hat', 'terjemahan': 'Topi', 'pelafalan': '(het)'}
    ],
    "Makanan": [
        {'kata': 'Bread', 'terjemahan': 'Roti', 'pelafalan': '(bred)'},
        {'kata': 'Rice', 'terjemahan': 'Nasi', 'pelafalan': '(rais)'},
        {'kata': 'Soup', 'terjemahan': 'Sup', 'pelafalan': '(sup)'},
        {'kata': 'Salad', 'terjemahan': 'Salad', 'pelafalan': '(seled)'},
        {'kata': 'Egg', 'terjemahan': 'Telur', 'pelafalan': '(eg)'}
    ],
    "Minuman": [
        {'kata': 'Water', 'terjemahan': 'Air', 'pelafalan': '(woter)'},
        {'kata': 'Milk', 'terjemahan': 'Susu', 'pelafalan': '(miluk)'},
        {'kata': 'Tea', 'terjemahan': 'Teh', 'pelafalan': '(ti)'},
        {'kata': 'Coffee', 'terjemahan': 'Kopi', 'pelafalan': '(kofi)'},
        {'kata': 'Juice', 'terjemahan': 'Jus', 'pelafalan': '(jus)'}
    ],
    "Profesi": [
        {'kata': 'Teacher', 'terjemahan': 'Guru', 'pelafalan': '(ticer)'},
        {'kata': 'Doctor', 'terjemahan': 'Dokter', 'pelafalan': '(doktor)'},
        {'kata': 'Engineer', 'terjemahan': 'Insinyur', 'pelafalan': '(enjinir)'},
        {'kata': 'Artist', 'terjemahan': 'Seniman', 'pelafalan': '(artis)'},
        {'kata': 'Chef', 'terjemahan': 'Koki', 'pelafalan': '(syef)'}
    ],
    "Negara": [
        {'kata': 'Indonesia', 'terjemahan': 'Indonesia', 'pelafalan': '(indonesia)'},
        {'kata': 'Japan', 'terjemahan': 'Jepang', 'pelafalan': '(jepen)'},
        {'kata': 'China', 'terjemahan': 'Tiongkok', 'pelafalan': '(caina)'},
        {'kata': 'USA', 'terjemahan': 'Amerika', 'pelafalan': '(yu es ei)'},
        {'kata': 'Germany', 'terjemahan': 'Jerman', 'pelafalan': '(jermani)'}
    ],
    "Olahraga": [
        {'kata': 'Football', 'terjemahan': 'Sepak bola', 'pelafalan': '(futbol)'},
        {'kata': 'Basketball', 'terjemahan': 'Bola basket', 'pelafalan': '(basketbol)'},
        {'kata': 'Swimming', 'terjemahan': 'Renang', 'pelafalan': '(swiming)'},
        {'kata': 'Tennis', 'terjemahan': 'Tenis', 'pelafalan': '(tenis)'},
        {'kata': 'Cycling', 'terjemahan': 'Bersepeda', 'pelafalan': '(saikling)'}
    ],
    "Keluarga": [
        {'kata': 'Father', 'terjemahan': 'Ayah', 'pelafalan': '(fader)'},
        {'kata': 'Mother', 'terjemahan': 'Ibu', 'pelafalan': '(mader)'},
        {'kata': 'Brother', 'terjemahan': 'Kakak/Adik Laki-laki', 'pelafalan': '(brader)'},
        {'kata': 'Sister', 'terjemahan': 'Kakak/Adik Perempuan', 'pelafalan': '(sister)'},
        {'kata': 'Grandmother', 'terjemahan': 'Nenek', 'pelafalan': '(grendmader)'}
    ],
    "Musim": [
        {'kata': 'Summer', 'terjemahan': 'Musim panas', 'pelafalan': '(samer)'},
        {'kata': 'Winter', 'terjemahan': 'Musim dingin', 'pelafalan': '(winter)'},
        {'kata': 'Spring', 'terjemahan': 'Musim semi', 'pelafalan': '(spring)'},
        {'kata': 'Autumn', 'terjemahan': 'Musim gugur', 'pelafalan': '(otem)'}
    ],
    "Cuaca": [
        {'kata': 'Sunny', 'terjemahan': 'Cerah', 'pelafalan': '(sani)'},
        {'kata': 'Cloudy', 'terjemahan': 'Berawan', 'pelafalan': '(klaudi)'},
        {'kata': 'Rainy', 'terjemahan': 'Hujan', 'pelafalan': '(reni)'},
        {'kata': 'Windy', 'terjemahan': 'Berangin', 'pelafalan': '(windi)'}
    ],
    "Perasaan": [
        {'kata': 'Happy', 'terjemahan': 'Senang', 'pelafalan': '(hepi)'},
        {'kata': 'Sad', 'terjemahan': 'Sedih', 'pelafalan': '(sed)'},
        {'kata': 'Angry', 'terjemahan': 'Marah', 'pelafalan': '(enggri)'},
        {'kata': 'Scared', 'terjemahan': 'Takut', 'pelafalan': '(skerd)'}
    ]
}

# ----------------- HELPERS -----------------

def text_to_speech(text: str) -> str:
    """Generate TTS MP3 and return path"""
    safe_name = text.replace(' ', '_')
    out_path = os.path.join(TEMP_AUDIO_DIR, f"{safe_name}.mp3")
    # If already exists, reuse
    if not os.path.exists(out_path):
        tts = gTTS(text=text, lang='en')
        tts.save(out_path)
    return out_path


def frames_to_wav_bytes(frames):
    """Convert a list of av.AudioFrame into WAV bytes (16-bit PCM mono)
    We rely on the frames having same sample rate and format.
    """
    if not frames:
        return None
    # Concatenate all frames as numpy and write to wav buffer
    sample_rate = frames[0].sample_rate
    pcm_arrays = []
    for frame in frames:
        # convert to ndarray (channels, samples)
        arr = frame.to_ndarray()
        # if stereo, average to mono
        if arr.ndim == 2:
            arr = arr.mean(axis=0)
        pcm_arrays.append(arr)
    concat = np.concatenate(pcm_arrays)
    # Ensure int16
    int16 = concat.astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int16.tobytes())
    buf.seek(0)
    return buf.read()

# ----------------- AUDIO PROCESSOR -----------------
class RecorderProcessor(AudioProcessorBase):
    """Audio processor that saves recent audio frames into an internal buffer.
    We'll expose `get_and_clear_recording()` to retrieve recorded frames for a short time window.
    """
    def __init__(self):
        self._frames = []
        self._lock = threading.Lock()

    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        # keep last N frames (we'll let streamlit front-end control duration by pressing record)
        with self._lock:
            self._frames.append(frame)
            # limit buffer (keep approx 5 seconds if sample_rate ~ 48000 and small frames)
            if len(self._frames) > 200:
                self._frames = self._frames[-200:]
        return frame

    def get_and_clear_recording(self):
        with self._lock:
            frames = list(self._frames)
            self._frames = []
        return frames

# ----------------- UI -----------------

st.title("📚 Kamus Kosakata Inggris-Indonesia — Full Version")
st.markdown("Pilih topik dari sidebar. Klik 🔊 untuk mendengar pengucapan; klik 🎙️ untuk merekam pengucapan Anda. Jika cocok dengan kosakata, akan muncul ✅.")

# Sidebar
st.sidebar.title("Pengaturan")
topic_list = list(vocab_data.keys())
selected_topic = st.sidebar.radio("Daftar Topik", topic_list)

st.header(f"Topik: {selected_topic}")

# Start one global webrtc streamer for STT so user doesn't have to create one per word.
# We'll use key 'global-webrtc' and create it in the sidebar area for compactness.
st.sidebar.markdown("---")
st.sidebar.markdown("**STT (microphone)**")
webrtc_ctx = webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDRECV,
    audio_receiver_size=256,
    media_stream_constraints={"audio": True, "video": False},
)

# Render vocabulary rows
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
        # TTS button
        tts_key = f"tts_{selected_topic}_{i}"
        if st.button("🔊", key=tts_key):
            path = text_to_speech(word)
            st.audio(path)

        # STT / Record button
        stt_key = f"stt_{selected_topic}_{i}"
        if st.button("🎙️", key=stt_key):
            # ensure we have a processor
            if webrtc_ctx and webrtc_ctx.state.playing and webrtc_ctx.audio_processor:
                processor = webrtc_ctx.audio_processor
                # retrieve frames recorded so far
                frames = processor.get_and_clear_recording()
                wav_bytes = frames_to_wav_bytes(frames)
                if wav_bytes is None:
                    st.warning("⚠️ Tidak ada audio yang direkam — coba tekan tombol 🎙️ lagi dan ucapkan selama 1-3 detik.")
                else:
                    # Use SpeechRecognition to transcribe
                    recognizer = sr.Recognizer()
                    with sr.AudioFile(io.BytesIO(wav_bytes)) as source:
                        audio_data = recognizer.record(source)
                    try:
                        recognized = recognizer.recognize_google(audio_data, language='en-US')
                        # Compare simple equality (case-insensitive). Remove punctuation
                        def normalize(s):
                            return ''.join(ch for ch in s.lower() if ch.isalnum() or ch.isspace()).strip()

                        if normalize(recognized) == normalize(word):
                            st.success(f"✅ Cocok! Anda mengucapkan: **{recognized}**")
                        else:
                            st.error(f"❌ Tidak cocok. Anda mengucapkan: **{recognized}**")
                            st.info(f"Target: **{word}**")

                    except sr.UnknownValueError:
                        st.warning("⚠️ Google Speech Recognition tidak bisa mengenali audio — coba kembali dengan suara yang lebih jelas.")
                    except sr.RequestError as e:
                        st.error(f"⚠️ Gagal terhubung ke layanan pengenalan suara: {e}")
            else:
                st.warning("⚠️ Microphone belum aktif. Pastikan Anda mengizinkan akses microphone di browser dan tunggu beberapa detik untuk inisialisasi WebRTC.")

st.markdown("---")
st.caption("Catatan: STT menggunakan Google Web Speech API lewat library SpeechRecognition. Kualitas transkripsi bergantung pada jaringan dan kondisi rekaman.")

# Cleanup: optional button to delete generated mp3 files (keamanan storage)
if st.sidebar.button('Bersihkan TTS cache'):
    files = os.listdir(TEMP_AUDIO_DIR)
    for f in files:
        try:
            os.remove(os.path.join(TEMP_AUDIO_DIR, f))
        except Exception:
            pass
    st.sidebar.success('Cache dibersihkan')

# End of file
