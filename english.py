import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Kamus Kosakata", layout="wide")

st.title("📚 Kamus Kosakata Inggris-Indonesia — TTS & STT")

# ======================
# Daftar 16 Topik
# ======================
topics = {
    "Hewan": [
        {"en": "cat", "id": "kucing"},
        {"en": "dog", "id": "anjing"},
        {"en": "bird", "id": "burung"},
    ],
    "Buah": [
        {"en": "apple", "id": "apel"},
        {"en": "banana", "id": "pisang"},
        {"en": "grape", "id": "anggur"},
    ],
    "Transportasi": [
        {"en": "car", "id": "mobil"},
        {"en": "train", "id": "kereta"},
        {"en": "bicycle", "id": "sepeda"},
    ],
    "Warna": [
        {"en": "red", "id": "merah"},
        {"en": "blue", "id": "biru"},
        {"en": "green", "id": "hijau"},
    ],
    "Anggota Tubuh": [
        {"en": "hand", "id": "tangan"},
        {"en": "eye", "id": "mata"},
        {"en": "leg", "id": "kaki"},
    ],
    "Pakaian": [
        {"en": "shirt", "id": "baju"},
        {"en": "pants", "id": "celana"},
        {"en": "hat", "id": "topi"},
    ],
    "Sekolah": [
        {"en": "book", "id": "buku"},
        {"en": "pen", "id": "pena"},
        {"en": "teacher", "id": "guru"},
    ],
    "Profesi": [
        {"en": "doctor", "id": "dokter"},
        {"en": "police", "id": "polisi"},
        {"en": "farmer", "id": "petani"},
    ],
    "Olahraga": [
        {"en": "soccer", "id": "sepak bola"},
        {"en": "basketball", "id": "bola basket"},
        {"en": "swimming", "id": "renang"},
    ],
    "Makanan": [
        {"en": "rice", "id": "nasi"},
        {"en": "bread", "id": "roti"},
        {"en": "chicken", "id": "ayam"},
    ],
    "Minuman": [
        {"en": "water", "id": "air"},
        {"en": "milk", "id": "susu"},
        {"en": "tea", "id": "teh"},
    ],
    "Keluarga": [
        {"en": "father", "id": "ayah"},
        {"en": "mother", "id": "ibu"},
        {"en": "sister", "id": "saudara perempuan"},
    ],
    "Peralatan": [
        {"en": "knife", "id": "pisau"},
        {"en": "spoon", "id": "sendok"},
        {"en": "chair", "id": "kursi"},
    ],
    "Arah": [
        {"en": "left", "id": "kiri"},
        {"en": "right", "id": "kanan"},
        {"en": "straight", "id": "lurus"},
    ],
    "Waktu": [
        {"en": "morning", "id": "pagi"},
        {"en": "afternoon", "id": "siang"},
        {"en": "night", "id": "malam"},
    ],
    "Cuaca": [
        {"en": "rain", "id": "hujan"},
        {"en": "sun", "id": "matahari"},
        {"en": "cloud", "id": "awan"},
    ],
}

# ======================
# Menu pilih topik
# ======================
topic_choice = st.sidebar.radio("📌 Pilih Topik", list(topics.keys()))

st.subheader(f"📖 Topik: {topic_choice}")

# ======================
# Tampilkan Vocabulary
# ======================
vocab_list = topics[topic_choice]

for vocab in vocab_list:
    en_word = vocab["en"]
    id_word = vocab["id"]

    st.markdown(f"### {en_word.capitalize()} — *{id_word}*")

    components.html(
        f"""
        <div style="margin-bottom:15px;">
            <!-- Tombol TTS -->
            <button onclick="speakWord('{en_word}')">🔊 TTS</button>
            
            <!-- Tombol STT -->
            <button onclick="startRecognition('{en_word}')">🎙️ STT</button>
            <span id="result_{en_word}" style="margin-left:10px; font-weight:bold; color:gray;"></span>
        </div>

        <script>
        // TTS
        function speakWord(word) {{
            var utterance = new SpeechSynthesisUtterance(word);
            utterance.lang = "en-US";
            speechSynthesis.speak(utterance);
        }}

        // STT
        function startRecognition(targetWord) {{
            var recognition = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = "en-US";
            recognition.start();

            recognition.onresult = function(event) {{
                var transcript = event.results[0][0].transcript.toLowerCase();
                var resultElem = document.getElementById("result_" + targetWord);

                if (transcript.includes(targetWord.toLowerCase())) {{
                    resultElem.innerHTML = "✅ Benar (" + transcript + ")";
                    resultElem.style.color = "green";
                }} else {{
                    resultElem.innerHTML = "❌ Salah (" + transcript + ")";
                    resultElem.style.color = "red";
                }}
            }};
        }}
        </script>
        """,
        height=80,
    )
