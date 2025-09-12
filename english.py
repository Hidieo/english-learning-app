import streamlit as st
import streamlit.components.v1 as components

st.title("🎙️ Live Speech-to-Text (Realtime Captions with Vocabulary Highlight)")

# Daftar vocabulary target
vocabulary = ["apple", "banana", "hello", "world", "computer"]

# Ubah list Python ke JavaScript array
vocab_js = str(vocabulary).replace("'", '"')

components.html(
    f"""
    <script>
    var recognizing;
    var recognition = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    var vocabulary = {vocab_js}; // daftar vocabulary dari Python

    recognition.onstart = function() {{
        document.getElementById('status').innerHTML = "🎤 Listening...";
    }};

    recognition.onend = function() {{
        document.getElementById('status').innerHTML = "🛑 Stopped";
    }};

    recognition.onresult = function(event) {{
        var interim_transcript = '';
        var final_transcript = '';
        for (var i = event.resultIndex; i < event.results.length; ++i) {{
            if (event.results[i].isFinal) {{
                final_transcript += event.results[i][0].transcript + " ";
            }} else {{
                interim_transcript += event.results[i][0].transcript + " ";
            }}
        }}

        // Highlight vocabulary
        final_transcript = highlightWords(final_transcript);
        interim_transcript = highlightWords(interim_transcript);

        document.getElementById('final').innerHTML = final_transcript;
        document.getElementById('interim').innerHTML = interim_transcript;
    }};

    function highlightWords(text) {{
        let words = text.split(/\\s+/);
        return words.map(w => {{
            if (vocabulary.includes(w.toLowerCase())) {{
                return "<span style='color:green; font-weight:bold;'>" + w + "</span>";
            }} else {{
                return w;
            }}
        }}).join(" ");
    }}

    function startButton() {{
        recognition.start();
    }}
    function stopButton() {{
        recognition.stop();
    }}
    </script>

    <button onclick="startButton()">▶️ Start</button>
    <button onclick="stopButton()">⏹ Stop</button>
    <p id="status">Not Listening</p>
    <h3>Final:</h3>
    <div id="final" style="font-size:18px;"></div>
    <h3>Interim:</h3>
    <div id="interim" style="font-size:16px; color:gray;"></div>
    """,
    height=450,
)
