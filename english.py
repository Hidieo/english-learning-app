import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase, RTCConfiguration
import speech_recognition as sr
import numpy as np
import av

# Konfigurasi WebRTC (penting untuk streamlit.io)
RTC_CONFIGURATION = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
})

class SpeechToTextProcessor(AudioProcessorBase):
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.text_output = ""

    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        # Convert ke numpy array
        audio = frame.to_ndarray().astype(np.int16)

        # Simpan ke temporary wav
        wav_path = "temp_audio/input.wav"
        import soundfile as sf
        sf.write(wav_path, audio, frame.sample_rate)

        # Coba transkrip dengan Google API
        with sr.AudioFile(wav_path) as source:
            audio_data = self.recognizer.record(source)
            try:
                result = self.recognizer.recognize_google(audio_data, language="en-US")
                self.text_output = result
            except sr.UnknownValueError:
                self.text_output = ""
            except sr.RequestError:
                self.text_output = "[ERROR: Google API tidak bisa diakses]"

        return frame


st.subheader("🎙️ Speech Recognition Realtime")
webrtc_ctx = webrtc_streamer(
    key="speech-to-text-demo",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    audio_processor_factory=SpeechToTextProcessor,
    media_stream_constraints={"audio": True, "video": False},
)

if webrtc_ctx.audio_processor:
    st.markdown("**Hasil Transkripsi:**")
    st.info(webrtc_ctx.audio_processor.text_output)
