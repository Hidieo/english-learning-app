import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Kamus Kosakata", layout="wide")

st.title("📚 Kamus Kosakata Inggris-Indonesia — TTS & STT")

# ======================
# Daftar Topik yang sudah diberikan
# ======================
topics = {
    "Topic 1 - Greeting & Expression": [
        {"en": "Good morning", "ph": "Gud mo-ning", "id": "Selamat pagi"},
        {"en": "Good afternoon", "ph": "Gud af-ter-nun", "id": "Selamat siang"},
        {"en": "Good evening", "ph": "Gud i-vning", "id": "Selamat malam"},
        {"en": "Sir", "ph": "Ser", "id": "Tuan"},
        {"en": "Madam", "ph": "Medem", "id": "Nyonya/Ibu"},
        {"en": "How are you?", "ph": "Hau ar yu?", "id": "Apa kabar"},
        {"en": "How can I help you?", "ph": "Hau ken ai help yu", "id": "Apa yang bisa saya bantu"},
        {"en": "May I have your name?", "ph": "Mei ai hev yor neim", "id": "Boleh saya tahu nama anda?"},
        {"en": "May I help with your luggage?", "ph": "Mei ai help wit yor lagij", "id": "Bolehkah saya membantu koper anda?"},
        {"en": "Please follow me", "ph": "Plis folou mi", "id": "Silahkan ikuti saya"},
        {"en": "Enjoy your stay", "ph": "Enjoi yor stei", "id": "Selamat menikmati masa menginap anda"},
        {"en": "Nice to meet you", "ph": "Nais tu mit yu", "id": "Senang bertemu anda"},
        {"en": "You’re welcome", "ph": "Yor welkom", "id": "Sama-sama"},
        {"en": "My pleasure", "ph": "Mai plezur", "id": "Senang bisa membantu"},
    ],
    "Topic 2a - Numbers": [
        {"en": "one", "ph": "wan", "id": "1"},
        {"en": "two", "ph": "twu", "id": "2"},
        {"en": "three", "ph": "thri", "id": "3"},
        {"en": "four", "ph": "for", "id": "4"},
        {"en": "five", "ph": "faiv", "id": "5"},
        {"en": "six", "ph": "siks", "id": "6"},
        {"en": "seven", "ph": "seven", "id": "7"},
        {"en": "eight", "ph": "eit", "id": "8"},
        {"en": "nine", "ph": "nain", "id": "9"},
        {"en": "ten", "ph": "ten", "id": "10"},
        {"en": "eleven", "ph": "ilevn", "id": "11"},
        {"en": "twelve", "ph": "twelv", "id": "12"},
        {"en": "thirteen", "ph": "thertin", "id": "13"},
        {"en": "fourteen", "ph": "forti:n", "id": "14"},
        {"en": "fifteen", "ph": "fifti:n", "id": "15"},
        {"en": "sixteen", "ph": "sixti:n", "id": "16"},
        {"en": "seventeen", "ph": "seventi:n", "id": "17"},
        {"en": "eighteen", "ph": "eiti:n", "id": "18"},
        {"en": "nineteen", "ph": "nainti:n", "id": "19"},
        {"en": "twenty", "ph": "twenti", "id": "20"},
    ],
    "Topic 2b - Ordinal Numbers": [
        {"en": "1st", "ph": "first", "id": "pertama"},
        {"en": "2nd", "ph": "second", "id": "kedua"},
        {"en": "3rd", "ph": "third", "id": "ketiga"},
        {"en": "4th", "ph": "fourth", "id": "keempat"},
        {"en": "5th", "ph": "fifth", "id": "kelima"},
        {"en": "6th", "ph": "sixth", "id": "keenam"},
        {"en": "7th", "ph": "seventh", "id": "ketujuh"},
        {"en": "8th", "ph": "eighth", "id": "kedelapan"},
        {"en": "9th", "ph": "ninth", "id": "kesembilan"},
        {"en": "10th", "ph": "tenth", "id": "kesepuluh"},
        {"en": "11th", "ph": "eleventh", "id": "kesebelas"},
        {"en": "12th", "ph": "twelfth", "id": "kedua belas"},
        {"en": "13th", "ph": "thirteenth", "id": "ketiga belas"},
        {"en": "14th", "ph": "fourteenth", "id": "keempat belas"},
        {"en": "15th", "ph": "fifteenth", "id": "kelima belas"},
        {"en": "16th", "ph": "sixteenth", "id": "keenam belas"},
        {"en": "17th", "ph": "seventeenth", "id": "ketujuh belas"},
        {"en": "18th", "ph": "eighteenth", "id": "kedelapan belas"},
        {"en": "19th", "ph": "nineteenth", "id": "kesembilan belas"},
        {"en": "20th", "ph": "twentieth", "id": "kedua puluh"},
    ],
    "Topic 2c - Days": [
        {"en": "Sunday", "ph": "sandei", "id": "Minggu"},
        {"en": "Monday", "ph": "mandei", "id": "Senin"},
        {"en": "Tuesday", "ph": "tyus-dei", "id": "Selasa"},
        {"en": "Wednesday", "ph": "wens-dei", "id": "Rabu"},
        {"en": "Thursday", "ph": "thers-dei", "id": "Kamis"},
        {"en": "Friday", "ph": "frai-dei", "id": "Jum'at"},
        {"en": "Saturday", "ph": "sader-dei", "id": "Sabtu"},
    ],
    "Topic 2d - Months": [
        {"en": "January", "ph": "janyu-eri", "id": "Januari"},
        {"en": "February", "ph": "febru-eri", "id": "Februari"},
        {"en": "March", "ph": "march", "id": "Maret"},
        {"en": "April", "ph": "eip-pril", "id": "April"},
        {"en": "May", "ph": "mey", "id": "Mei"},
        {"en": "June", "ph": "jun", "id": "Juni"},
        {"en": "July", "ph": "julai", "id": "Juli"},
        {"en": "August", "ph": "ogos", "id": "Agustus"},
        {"en": "September", "ph": "septembe", "id": "September"},
        {"en": "October", "ph": "octoube", "id": "Oktober"},
        {"en": "November", "ph": "novembe", "id": "November"},
        {"en": "December", "ph": "di-sembe", "id": "Desember"},
    ],
    "Topic 2e - Time Expressions": [
        {"en": "o'clock", "ph": "o'klok", "id": "tepat dari jam 12 malam sampai 12 siang"},
        {"en": "a.m.", "ph": "ei-em", "id": "jam 12 malam ke jam 12 siang"},
        {"en": "p.m.", "ph": "pi-em", "id": "jam 12 siang ke jam 12 malam"},
        {"en": "quarter past", "ph": "kwar-ter pas", "id": "lewat 15 menit"},
        {"en": "half past", "ph": "half-pas", "id": "lewat 30 menit"},
        {"en": "quarter to", "ph": "kwar-ter twu", "id": "kurang 15 menit"},
        {"en": "noon", "ph": "nun", "id": "tengah hari"},
        {"en": "midday", "ph": "mid-dei", "id": "tengah hari"},
        {"en": "opening hours", "ph": "opening awers", "id": "jam buka"},
        {"en": "closing time", "ph": "klosing taim", "id": "jam tutup"},
        {"en": "check-in time", "ph": "check-in taim", "id": "waktu check-in (masuk)"},
        {"en": "check-out time", "ph": "check-aut taim", "id": "waktu check-out (keluar)"},
        {"en": "1 O'clock", "ph": "wan o'klok", "id": "jam 1"},
        {"en": "2.15", "ph": "twu fiftin", "id": "jam 2 lewat 15"},
        {"en": "Two fifteen", "ph": "e kwar-ter pas twu", "id": "jam 2 lewat 15"},
        {"en": "A quarter past two", "ph": "e kwar-ter pas twu", "id": "jam 2 lewat 15"},
        {"en": "Two thirty", "ph": "twu ther-ti", "id": "jam 2.30"},
        {"en": "A half past two", "ph": "e half past twu", "id": "jam 2.30"},
        {"en": "Two forty five", "ph": "twu fo-ti faiv", "id": "jam 2.45"},
        {"en": "A quarter to three", "ph": "e kwar-ter twu thri", "id": "jam 2.45"},
    ],
    "Topic 3 - Hotel Jobs": [
        {"en": "General manager", "ph": "Jen-rel menejer", "id": "Manajer umum"},
        {"en": "Front office manager", "ph": "Front ofis menejer", "id": "Manajer front office"},
        {"en": "Receptionist", "ph": "Risep-sye-nis", "id": "Resepsionis"},
        {"en": "Concierge", "ph": "Kon-syerj", "id": "Petugas concierge"},
        {"en": "Bell boy / bell attendant", "ph": "Bel boi / bel atendan", "id": "Petugas pembawa barang"},
        {"en": "Porter", "ph": "Por-ter", "id": "Porter"},
        {"en": "Room attendant", "ph": "Rum aten-dan", "id": "Petugas kebersihan kamar"},
        {"en": "Housekeeping Supervisor", "ph": "Haus-kiping super-vaizer", "id": "Pengawas housekeeping"},
        {"en": "Laundry attendant", "ph": "Lon-dri atendan", "id": "Petugas laundry"},
        {"en": "Waiter / waitress", "ph": "Wai-ter / wei-tres", "id": "Pramusaji"},
        {"en": "Bartender", "ph": "Bar-ten-der", "id": "Bartender"},
        {"en": "Banquet manager", "ph": "Ben-kuet menejer", "id": "Manajer Banquet"},
        {"en": "Maintenance Technician", "ph": "Mein-tenens tek-ni-syen", "id": "Teknisi pemeliharaan"},
        {"en": "Security officer", "ph": "Si-kiu-riti ofiser", "id": "Petugas keamanan"},
        {"en": "Spa therapist", "ph": "Spa terap-is", "id": "Terapis spa"},
        {"en": "Lifeguard", "ph": "Laif-gard", "id": "Penjaga kolam"},
        {"en": "Sales and Marketing Manager", "ph": "Seils en marketing menejer", "id": "Manajer penjualan dan pemasaran"},
        {"en": "Event Coordinator", "ph": "Iven koor-dinetor", "id": "Koordinator acara"},
    ],
}

# ======================
# Menu pilih topik
# ======================
topic_choice = st.sidebar.radio("📌 Pilih Topik", list(topics.keys()))

st.subheader(f"📖 {topic_choice}")

# ======================
# Tampilkan Vocabulary
# ======================
vocab_list = topics[topic_choice]

for vocab in vocab_list:
    en_word = vocab["en"]
    ph_word = vocab["ph"]
    id_word = vocab["id"]

    st.markdown(f"### {en_word} ({ph_word}) — *{id_word}*")

    components.html(
        f"""
        <div style="margin-bottom:15px;">
            <!-- Tombol TTS -->
            <button onclick="speakWord('{en_word}')">🔊 TTS</button>
            
            <!-- Tombol STT -->
            <button onclick="startRecognition('{en_word}')">🎙️ STT</button>
            <span id="result_{en_word.replace(" ", "_")}" style="margin-left:10px; font-weight:bold; color:gray;"></span>
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
                var resultElem = document.getElementById("result_" + targetWord.replace(/ /g,"_"));

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
