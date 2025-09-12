import streamlit as st
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval

# Daftar kosakata (contoh kecil)
vocab_words = [v["kata"].lower() for topic in vocab_data.values() for v in topic]

st.title("🎙️ Live Speech-to-Text with Vocabulary Matching")

# Komponen HTML untuk Web Speech API
components.html(
    """
    <script>
    var recognizing;
    var recognition = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    recognition.onresult = function(event) {
        var interim_transcript = '';
        var final_transcript = '';
        for (var i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                final_transcript += event.results[i][0].transcript;
            } else {
                interim_transcript += event.results[i][0].transcript;
            }
        }
        // Kirim hasil final ke Python
        const streamlitDoc = window.parent.document;
        const input = streamlitDoc.querySelector('textarea[data-testid="stTextInput-input"]');
        if (input) {
            input.value = final_transcript;
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
    };

    function startButton() {
        recognition.start();
    }
    function stopButton() {
        recognition.stop();
    }
    </script>

    <button onclick="startButton()">▶️ Start</button>
    <button onclick="stopButton()">⏹ Stop</button>
    """,
    height=150,
)

# Input tersembunyi buat menampung hasil transkrip
transcript = st.text_input("Hidden transcript", key="speech_text")

if transcript:
    st.markdown(f"📝 Teks terdeteksi: **{transcript}**")

    words = transcript.lower().split()
    matched = [w for w in words if w in vocab_words]

    if matched:
        for w in words:
            if w in matched:
                st.markdown(f"<span style='color:green; font-weight:bold'>{w}</span>", unsafe_allow_html=True)
            else:
                st.markdown(w, unsafe_allow_html=True)
    else:
        st.warning("❌ Tidak ada kata yang cocok dengan kosakata.")
