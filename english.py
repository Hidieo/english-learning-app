from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import speech_recognition as sr

# Fungsi untuk menangani audio stream
def audio_callback(frame: av.AudioFrame) -> av.AudioFrame:
    audio = frame.to_ndarray()
    return frame

st.subheader("🎙️ Ucapkan kata untuk dikenali:")

webrtc_ctx = webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=1024,
    media_stream_constraints={"audio": True, "video": False},
    async_processing=True,
)

if webrtc_ctx.audio_receiver:
    try:
        audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
        for audio_frame in audio_frames:
            # Simpan audio ke file sementara
            wav_path = f"{TEMP_AUDIO_DIR}/temp_input.wav"
            audio_frame.to_ndarray().tofile(wav_path)

            # Panggil SpeechRecognition
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language="en-US")
                    st.success(f"Terdeteksi: {text}")
                except sr.UnknownValueError:
                    st.warning("Tidak bisa mengenali suara.")
    except Exception as e:
        st.error(f"Error: {e}")
