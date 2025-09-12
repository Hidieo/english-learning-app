import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import speech_recognition as sr
import av
import numpy as np

st.set_page_config(page_title="🎤 STT Realtime WebRTC", layout="centered")

st.title("🎙️ Speech-to-Text Realtime dengan WebRTC")
st.markdown(
    """
    > Klik tombol **Start** di bawah untuk mengaktifkan microphone.  
    > Ucapkan sesuatu, hasil transkripsi akan muncul secara realtime.  
    """
)

# Audio Processor
class STTProcessor(AudioProcessorBase):
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.text = "Belum ada input suara..."

    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        # Convert frame ke numpy array
        audio = frame.to_ndarray().flatten().astype(np.int16).tobytes()

        # Proses audio dengan SpeechRecognition
        try:
            audio_data = sr.AudioData(audio, frame.sample_rate, 2)
            recognized = self.recognizer.recognize_google(audio_data, language="id-ID")
            self.text = recognized
        except sr.UnknownValueError:
            pass  # kalau belum jelas jangan error
        except Exception as e:
            self.text = f"Error: {e}"

        return frame

# Jalankan WebRTC
ctx = webrtc_streamer(
    key="stt",
    mode=WebRtcMode.SENDONLY,
    audio_processor_factory=STTProcessor,
    media_stream_constraints={"audio": True, "video": False},
)

# Tampilkan hasil
if ctx.audio_processor:
    st.markdown("### 📝 Hasil Transkripsi")
    st.info(ctx.audio_processor.text)
