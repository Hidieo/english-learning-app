# app.py
# -*- coding: utf-8 -*-
"""
Kamus Kosakata Interaktif + Real-time STT (DeepSpeech) via streamlit-webrtc
"""

import os
import queue
import time
import urllib.request
from pathlib import Path
from collections import deque
import difflib

import streamlit as st
from gtts import gTTS

# realtime audio libs
import av
import numpy as np
import pydub
from streamlit_webrtc import WebRtcMode, webrtc_streamer

# DeepSpeech import is inside functions to avoid import error until model is downloaded
# from deepspeech import Model

HERE = Path(__file__).parent

# Temporary audio directory
TEMP_AUDIO_DIR = "temp_audio"
if not os.path.exists(TEMP_AUDIO_DIR):
    os.makedirs(TEMP_AUDIO_DIR)

# --- VOCAB DATA (sama seperti yang kamu kirim) ---
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

# --- STYLES (sederhana) ---
st.set_page_config(page_title="Kamus Kosakata Interaktif", page_icon="📚", layout="centered")

st.markdown("""
<style>
    .stButton>button { background-color:#1e88e5;color:white;border-radius:6px; }
</style>
""", unsafe_allow_html=True)


# --- DeepSpeech model download utilities (sama konsepnya dengan referensi) ---
MODEL_URL = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm"
SCORER_URL = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer"
MODEL_LOCAL_PATH = HERE / "models/deepspeech-0.9.3-models.pbmm"
SCORER_LOCAL_PATH = HERE / "models/deepspeech-0.9.3-models.scorer"


def download_file(url, download_to: Path, expected_size=None):
    if download_to.exists():
        return
    download_to.parent.mkdir(parents=True, exist_ok=True)
    weights_warning = st.empty()
    progress_bar = st.progress(0)
    try:
        with urllib.request.urlopen(url) as response:
            length = int(response.info().get("Content-Length", -1))
            with open(download_to, "wb") as output_file:
                counter = 0
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    output_file.write(chunk)
                    counter += len(chunk)
                    if length > 0:
                        progress_bar.progress(min(counter / length, 1.0))
                        weights_warning.info(f"Downloading {url}... ({counter // (2**20)} MB)")
    finally:
        progress_bar.empty()
        weights_warning.empty()


@st.cache_data
def get_ice_servers():
    # fallback to google stun if no Twilio env vars
    try:
        from twilio.rest import Client
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        client = Client(account_sid, auth_token)
        token = client.tokens.create()
        return token.ice_servers
    except Exception:
        return [{"urls": ["stun:stun.l.google.com:19302"]}]


# Load DeepSpeech model once (cached)
@st.cache_resource
def load_deepspeech_model(model_path: str, scorer_path: str):
    from deepspeech import Model
    model = Model(model_path)
    if scorer_path and os.path.exists(scorer_path):
        model.enableExternalScorer(scorer_path)
    # recommended params (from reference)
    model.setScorerAlphaBeta(0.931289039105002, 1.1834137581510284)
    model.setBeamWidth(100)
    return model


# Simple similarity check using difflib
def similarity(a: str, b: str) -> float:
    a_norm = a.strip().lower()
    b_norm = b.strip().lower()
    return difflib.SequenceMatcher(None, a_norm, b_norm).ratio()


# --- TTS function (gTTS) ---
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    path = f"{TEMP_AUDIO_DIR}/temp_{int(time.time()*1000)}.mp3"
    with open(path, "wb") as f:
        tts.write_to_fp(f)
    return path


# --- STT (webrtc + deepspeech) functions ---
def app_sst_soundonly(target_word: str | None = None):
    """
    Sound-only STT using webrtc_streamer in SENDONLY mode.
    If target_word provided, compare recognition result to target_word.
    """
    ice = get_ice_servers()
    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        rtc_configuration={"iceServers": ice},
        media_stream_constraints={"video": False, "audio": True},
    )

    status_indicator = st.empty()
    text_output = st.empty()
    if not webrtc_ctx.state.playing:
        return

    # lazy load model (download if not exists)
    if not MODEL_LOCAL_PATH.exists() or not SCORER_LOCAL_PATH.exists():
        st.info("Model DeepSpeech tidak ditemukan. Mulai mendownload (besar - butuh waktu).")
        download_file(MODEL_URL, MODEL_LOCAL_PATH)
        download_file(SCORER_URL, SCORER_LOCAL_PATH)

    ds_model = load_deepspeech_model(str(MODEL_LOCAL_PATH), str(SCORER_LOCAL_PATH))
    stream = None

    stream = ds_model.createStream()
    status_indicator.info("Model loaded. Silakan mulai berbicara... (akan muncul transkrip semuanya realtime)")

    while webrtc_ctx.state.playing:
        if webrtc_ctx.audio_receiver:
            try:
                audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
            except queue.Empty:
                time.sleep(0.1)
                continue

            sound_chunk = pydub.AudioSegment.empty()

            for audio_frame in audio_frames:
                sound = pydub.AudioSegment(
                    data=audio_frame.to_ndarray().tobytes(),
                    sample_width=audio_frame.format.bytes,
                    frame_rate=audio_frame.sample_rate,
                    channels=len(audio_frame.layout.channels),
                )
                sound_chunk += sound

            if len(sound_chunk) > 0:
                # convert to mono & sample rate expected by model
                sound_chunk = sound_chunk.set_channels(1).set_frame_rate(ds_model.sampleRate())
                buffer = np.array(sound_chunk.get_array_of_samples())
                stream.feedAudioContent(buffer)
                text = stream.intermediateDecode()
                if text is None:
                    text = ""
                text_output.markdown(f"**Transkrip (sementara):** {text}")

                if target_word and text.strip() != "":
                    sim = similarity(text, target_word)
                    pct = int(sim * 100)
                    if sim >= 0.85:
                        st.success(f"✅ Pengucapan baik (similarity {pct}%)")
                    elif sim >= 0.6:
                        st.warning(f"⚠️ Hampir benar (similarity {pct}%)")
                    else:
                        st.error(f"❌ Salah (similarity {pct}%). Seharusnya: **{target_word}**")
        else:
            status_indicator.error("AudioReceiver belum tersedia. Pastikan browser membuka mikrofon.")
            break


# --- MAIN UI ---
def main():
    st.title("📚 Kamus Kosakata Inggris-Indonesia (TTS + STT Microphone)")
    st.markdown("Pilih topik di sidebar. Tekan 🔊 untuk dengar, atau 🎙️ untuk coba ucapkan lewat mikrofon (real-time).")

    # Sidebar
    st.sidebar.title("Pengaturan")
    theme_option = st.sidebar.radio("Pilih Tema Latar", ("Terang (Default)", "Gelap"))
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
            st.markdown(f"*{translation}* {pronunciation}")
        with col3:
            # TTS button
            if st.button("🔊", key=f"tts_{word}_{i}"):
                audio_path = text_to_speech(word)
                with open(audio_path, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
                try:
                    os.remove(audio_path)
                except Exception:
                    pass

            # STT button - launches the webrtc STT panel in the page
            if st.button("🎙️ Coba Ucapkan", key=f"stt_{word}_{i}"):
                st.info(f"Mulai ucapkan kata: **{word}**. Klik Stop di control WebRTC di pojok kanan atas (jika ada).")
                app_sst_soundonly(target_word=word)

    st.markdown("---")
    st.caption("Catatan: Model DeepSpeech akan didownload saat pertama kali digunakan (besar). Jika ingin cepat, gunakan model STT alternatif atau pre-download model ke folder 'models/'.")

if __name__ == "__main__":
    main()
