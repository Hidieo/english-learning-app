import streamlit as st
import streamlit.components.v1 as components

st.title("🎙️ Live Speech-to-Text (Realtime Captions)")

# Komponen HTML + JS untuk Web Speech API
components.html(
    """
    <script>
    var recognizing;
    var recognition = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    recognition.onstart = function() {
        document.getElementById('status').innerHTML = "🎤 Listening...";
    };

    recognition.onend = function() {
        document.getElementById('status').innerHTML = "🛑 Stopped";
    };

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
        document.getElementById('final').innerHTML = final_transcript;
        document.getElementById('interim').innerHTML = interim_transcript;
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
    <p id="status">Not Listening</p>
    <h3>Final:</h3>
    <div id="final" style="color:green; font-weight:bold;"></div>
    <h3>Interim:</h3>
    <div id="interim" style="color:gray;"></div>
    """,
    height=400,
)
