import streamlit as st
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval

st.title("🎙️ Live Speech-to-Text (Realtime Captions)")

if "recognized_text" not in st.session_state:
    st.session_state.recognized_text = ""

components.html(
    """
    <script>
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    recognition.onresult = function(event) {
        var transcript = '';
        for (var i = event.resultIndex; i < event.results.length; ++i) {
            transcript += event.results[i][0].transcript;
        }
        // kirim ke Streamlit (streamlit-js-eval akan tangkap)
        window.parent.postMessage({isStreamlitMessage:true, type:"streamlit:setComponentValue", value:transcript}, "*");
    };

    function startSTT() { recognition.start(); }
    function stopSTT() { recognition.stop(); }
    </script>

    <button onclick="startSTT()">▶️ Start</button>
    <button onclick="stopSTT()">⏹ Stop</button>
    <p>🎤 Klik Start lalu ucapkan kata</p>
    """,
    height=180,
)

# Ambil data dari JS → Python
captions = streamlit_js_eval(js_expressions="null", key="speech_to_text")

if captions:
    st.session_state.recognized_text = captions

st.subheader("Hasil Transkripsi 🎤")
st.info(st.session_state.recognized_text)
