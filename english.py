import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.title("🎙️ Live Speech-to-Text (Realtime Captions)")

# Siapkan state untuk teks
if "captions" not in st.session_state:
    st.session_state["captions"] = ""

# Komponen HTML + JS (pakai Web Speech API)
st.markdown(
    """
    <script>
    function startSTT() {
        var recognition = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "en-US";

        recognition.onresult = function(event) {
            var interim_transcript = '';
            var final_transcript = '';
            for (var i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    final_transcript += event.results[i][0].transcript + " ";
                } else {
                    interim_transcript += event.results[i][0].transcript;
                }
            }
            // kirim ke Python via streamlit-js-eval
            const combined = final_transcript + " " + interim_transcript;
            window.parent.postMessage(
                {isStreamlitMessage:true, type:"streamlit:setComponentValue", value:combined},
                "*"
            );
        };

        recognition.start();
    }
    </script>
    <button onclick="startSTT()">▶️ Start Listening</button>
    """,
    unsafe_allow_html=True,
)

# Ambil hasil dari JS
captions = streamlit_js_eval(
    js_expressions="null", 
    key="speech_eval"
)

if captions:
    st.session_state["captions"] = captions

st.subheader("📝 Hasil Transkripsi")
st.info(st.session_state["captions"])
