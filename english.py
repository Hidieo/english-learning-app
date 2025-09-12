# -*- coding: utf-8 -*-
"""Kamus Kosakata Interaktif v2.0 - Stable WebRTC

This script implements a full Streamlit application for an interactive English-Indonesian
vocabulary dictionary with stable WebRTC-based Speech-to-Text (STT) functionality.
"""

import streamlit as st
import gtts
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

# --- KONFIGURASI APLIKASI ---
TEMP_AUDIO_DIR = "temp_audio"
if not os.path.exists(TEMP_AUDIO_DIR):
    os.makedirs(TEMP_AUDIO_DIR)

st.set_page_config(
    page_title="Kamus Kosakata Interaktif",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Kustomisasi CSS untuk perpaduan biru dan putih
st.markdown("""
<style>
    /* Mengubah warna sidebar */
    .st-emotion-cache-121bd7t.e1ds3rsq1 {
        background-color: #f0f2f6;
        color: #0d47a1;
    }
    
    /* Warna teks di sidebar */
    .st-emotion-cache-vk3ypu.e1ds3rsq3 {
        color: #0d47a1;
    }
    
    /* Warna background utama */
    .st-emotion-cache-1cypj85.e1ds3rsq0 {
        background-color: #ffffff;
    }
    
    /* Kustomisasi button */
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
    
    /* Button untuk TTS & STT */
    .stButton > button {
        background-color: #1e88e5; /* Biru terang */
        color: white;
        border-radius: 5px;
        border: none;
        padding: 8px 12px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #2196f3; /* Biru yang lebih terang saat hover */
    }

</style>
""", unsafe_allow_html=True)

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

# --- FUNGSI-FUNGSI UTAMA ---
def text_to_speech(text: str) -> str:
    """Mengubah teks menjadi file audio MP3."""
    safe_name = text.replace(' ', '_')
    out_path = os.path.join(TEMP_AUDIO_DIR, f"{safe_name}.mp3")
    if not os.path.exists(out_path):
        tts = gTTS(text=text, lang='en')
        tts.save(out_path)
    return out_path

def frames_to_wav_bytes(frames):
    """Mengubah frames audio dari WebRTC menjadi format WAV bytes."""
    if not frames:
        return None
    sample_rate = frames[0].sample_rate
    pcm_arrays = [frame.to_ndarray().mean(axis=0) if frame.to_ndarray().ndim == 2 else frame.to_ndarray() for frame in frames]
    concat = np.concatenate(pcm_arrays).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(concat.tobytes())
    buf.seek(0)
    return buf.read()

def normalize_text(s: str) -> str:
    """Menghilangkan karakter non-alfanumerik untuk perbandingan."""
    return ''.join(ch for ch in s.lower() if ch.isalnum() or ch.isspace()).strip()

# --- AUDIO PROCESSOR UNTUK STREAMLIT-WEBRTC ---
class RecorderProcessor(AudioProcessorBase):
    def __init__(self):
        self._frames = []
        self._lock = threading.Lock()
        self.last_audio_time = time.time()

    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        arr = frame.to_ndarray()
        if arr.ndim == 2:
            arr = arr[:, 0]
        
        with self._lock:
            self._frames.append(frame)
            # Batasi buffer ke 3-4 detik
            if len(self._frames) > 250:  
                self._frames = self._frames[-250:]
        
        self.last_audio_time = time.time()
        return frame

    def get_and_clear_recording(self):
        with self._lock:
            frames = list(self._frames)
            self._frames = []
        return frames

# --- ANTARMUKA UTAMA STREAMLIT ---
st.title("📚 Kamus Kosakata Inggris-Indonesia — WebRTC STT")
st.markdown("""
<p style="color:#666666;">
Instruksi: Pilih topik di sidebar. Klik **Start** pada widget WebRTC, izinkan microphone, tunggu 2-3 detik, lalu tekan tombol 🎙️ di kata yang ingin direkam.
</p>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Pengaturan & STT (Mic)")
topic_list = list(vocab_data.keys())
selected_topic = st.sidebar.radio("Pilih Topik", topic_list)
st.sidebar.markdown("---")

st.sidebar.markdown("**Kontrol WebRTC / Microphone**")
webrtc_ctx = webrtc_streamer(
    key="speech-to-text-global",
    mode=WebRtcMode.SENDRECV,
    audio_processor_factory=RecorderProcessor,
    media_stream_constraints={ "audio": True, "video": False },
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    async_processing=True,
    audio_receiver_size=256
)

if webrtc_ctx.state.playing:
    st.sidebar.success("WebRTC: microphone aktif ✅")
else:
    st.sidebar.info("WebRTC: Tekan 'Start' dan izinkan microphone.")

# Placeholder untuk pesan feedback
message_placeholder = st.empty()

# Tampilkan kosakata
st.header(f"Topik: {selected_topic}")
st.markdown("Klik 🔊 untuk mendengar kata. Klik 🎙️ untuk merekam & cek pengucapan.")

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
        if st.button("🔊", key=f"tts_{selected_topic}_{i}"):
            path = text_to_speech(word)
            st.audio(path)
        
        if st.button("🎙️", key=f"stt_{selected_topic}_{i}"):
            if not (webrtc_ctx and webrtc_ctx.state.playing and webrtc_ctx.audio_processor):
                message_placeholder.warning("⚠️ WebRTC belum aktif / mic belum diizinkan.")
            else:
                message_placeholder.info("🗣️ Sedang merekam... Mohon ucapkan kata sekarang.")
                
                # Jeda singkat untuk memastikan audio diambil
                time.sleep(1) 
                
                with st.spinner("Memproses rekaman..."):
                    processor = webrtc_ctx.audio_processor
                    frames = processor.get_and_clear_recording()
                    
                    if not frames:
                        message_placeholder.warning("⚠️ Tidak ada audio yang terdeteksi. Coba lagi dan bicara lebih dekat.")
                        continue
                    
                    wav_bytes = frames_to_wav_bytes(frames)
                    st.audio(wav_bytes, format="audio/wav")

                    recognizer = sr.Recognizer()
                    try:
                        with sr.AudioFile(io.BytesIO(wav_bytes)) as source:
                            audio_data = recognizer.record(source)
                        
                        recognized = recognizer.recognize_google(audio_data, language='en-US')
                        
                        if normalize_text(recognized) == normalize_text(word):
                            message_placeholder.success(f"✅ Cocok! Anda mengucapkan: **{recognized}**")
                        else:
                            message_placeholder.error(f"❌ Tidak cocok. Anda mengucapkan: **{recognized}**")
                            st.info(f"Target: **{word}**")

                    except sr.UnknownValueError:
                        message_placeholder.warning("⚠️ Google tidak bisa mengenali audio.")
                    except Exception as e:
                        message_placeholder.error(f"⚠️ Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()
