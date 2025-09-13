import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Kamus Kosakata", layout="wide")

st.title("📚 Kamus Kosakata Inggris-Indonesia — TTS & STT")

# ======================
# Daftar Topik yang sudah diberikan
# ======================
topics = {
    "Topic 1 - Greeting & Expression": [
    {"english": "Good morning", "phonetic": "Gud mo-ning", "indonesia": "Selamat pagi"},
    {"english": "Good afternoon", "phonetic": "Gud af-ter-nun", "indonesia": "Selamat siang"},
    {"english": "Good evening", "phonetic": "Gud i-vning", "indonesia": "Selamat malam"},
    {"english": "Sir", "phonetic": "Ser", "indonesia": "Tuan"},
    {"english": "Madam", "phonetic": "Medem", "indonesia": "Nyonya/Ibu"},
    {"english": "How are you?", "phonetic": "Hau ar yu?", "indonesia": "Apa kabar"},
    {"english": "How can I help you?", "phonetic": "Hau ken ai help yu", "indonesia": "Apa yang bisa saya bantu"},
    {"english": "May I have your name?", "phonetic": "Mei ai hev yor neim", "indonesia": "Boleh saya tahu nama anda?"},
    {"english": "May I help with your luggage?", "phonetic": "Mei ai help wit yor lagij", "indonesia": "Bolehkah saya membantu koper anda?"},
    {"english": "Please follow me", "phonetic": "Plis folou mi", "indonesia": "Silahkan ikuti saya"},
    {"english": "Enjoy your stay", "phonetic": "Enjoi yor stei", "indonesia": "Selamat menikmati masa menginap anda"},
    {"english": "Nice to meet you", "phonetic": "Nais tu mit yu", "indonesia": "Senang bertemu anda"},
    {"english": "You’re welcome", "phonetic": "Yor welkom", "indonesia": "Sama-sama"},
    {"english": "My pleasure", "phonetic": "Mai plezur", "indonesia": "Senang bisa membantu"}
],
    "Topic 2a - Numbers": [
        {"english": "1", "phonetic": "wan", "indonesia": "satu"},
        {"english": "2", "phonetic": "twu", "indonesia": "dua"},
        {"english": "3", "phonetic": "thri", "indonesia": "tiga"},
        {"english": "4", "phonetic": "for", "indonesia": "empat"},
        {"english": "5", "phonetic": "faiv", "indonesia": "lima"},
        {"english": "6", "phonetic": "siks", "indonesia": "enam"},
        {"english": "7", "phonetic": "seven", "indonesia": "tujuh"},
        {"english": "8", "phonetic": "eit", "indonesia": "delapan"},
        {"english": "9", "phonetic": "nain", "indonesia": "sembilan"},
        {"english": "10", "phonetic": "ten", "indonesia": "sepuluh"},
        {"english": "11", "phonetic": "ilevn", "indonesia": "sebelas"},
        {"english": "12", "phonetic": "twelv", "indonesia": "duabelas"},
        {"english": "13", "phonetic": "thertin", "indonesia": "tigabelas"},
        {"english": "14", "phonetic": "forti:n", "indonesia": "empatbelas"},
        {"english": "15", "phonetic": "fifti:n", "indonesia": "limabelas"},
        {"english": "16", "phonetic": "sixti:n", "indonesia": "enambelas"},
        {"english": "17", "phonetic": "seventi:n", "indonesia": "tujuhbelas"},
        {"english": "18", "phonetic": "eiti:n", "indonesia": "delapanbelas"},
        {"english": "19", "phonetic": "nainti:n", "indonesia": "sembilanbelas"},
        {"english": "20", "phonetic": "twenti", "indonesia": "duapuluh"}
    ],
    "Topic 2b - Ordinal Numbers": [
        {"english": "1st", "phonetic": "first", "indonesia": "pertama"},
        {"english": "2nd", "phonetic": "second", "indonesia": "kedua"},
        {"english": "3rd", "phonetic": "third", "indonesia": "ketiga"},
        {"english": "4th", "phonetic": "fourth", "indonesia": "keempat"},
        {"english": "5th", "phonetic": "fifth", "indonesia": "kelima"},
        {"english": "6th", "phonetic": "sixth", "indonesia": "keenam"},
        {"english": "7th", "phonetic": "seventh", "indonesia": "ketujuh"},
        {"english": "8th", "phonetic": "eighth", "indonesia": "kedelapan"},
        {"english": "9th", "phonetic": "ninth", "indonesia": "kesembilan"},
        {"english": "10th", "phonetic": "tenth", "indonesia": "kesepuluh"},
        {"english": "11th", "phonetic": "eleventh", "indonesia": "kesebelas"},
        {"english": "12th", "phonetic": "twelfth", "indonesia": "kedua belas"},
        {"english": "13th", "phonetic": "thirteenth", "indonesia": "ketiga belas"},
        {"english": "14th", "phonetic": "fourteenth", "indonesia": "keempat belas"},
        {"english": "15th", "phonetic": "fifteenth", "indonesia": "kelima belas"},
        {"english": "16th", "phonetic": "sixteenth", "indonesia": "keenam belas"},
        {"english": "17th", "phonetic": "seventeenth", "indonesia": "ketujuh belas"},
        {"english": "18th", "phonetic": "eighteenth", "indonesia": "kedelapan belas"},
        {"english": "19th", "phonetic": "nineteenth", "indonesia": "kesembilan belas"},
        {"english": "20th", "phonetic": "twentieth", "indonesia": "kedua puluh"}
    ],
    "Topic 2c - Days": [
        {"english": "Sunday", "phonetic": "sandei", "indonesia": "Minggu"},
        {"english": "Monday", "phonetic": "mandei", "indonesia": "Senin"},
        {"english": "Tuesday", "phonetic": "tyus-dei", "indonesia": "Selasa"},
        {"english": "Wednesday", "phonetic": "wens-dei", "indonesia": "Rabu"},
        {"english": "Thursday", "phonetic": "thers-dei", "indonesia": "Kamis"},
        {"english": "Friday", "phonetic": "frai-dei", "indonesia": "Jum'at"},
        {"english": "Saturday", "phonetic": "sader-dei", "indonesia": "Sabtu"},
    ],
    "Topic 2d - Months": [
        {"english": "January", "phonetic": "janyu-eri", "indonesia": "Januari"},
        {"english": "February", "phonetic": "febru-eri", "indonesia": "Februari"},
        {"english": "March", "phonetic": "march", "indonesia": "Maret"},
        {"english": "April", "phonetic": "eip-pril", "indonesia": "April"},
        {"english": "May", "phonetic": "mey", "indonesia": "Mei"},
        {"english": "June", "phonetic": "jun", "indonesia": "Juni"},
        {"english": "July", "phonetic": "julai", "indonesia": "Juli"},
        {"english": "August", "phonetic": "ogos", "indonesia": "Agustus"},
        {"english": "September", "phonetic": "septembe", "indonesia": "September"},
        {"english": "October", "phonetic": "octoube", "indonesia": "Oktober"},
        {"english": "November", "phonetic": "novembe", "indonesia": "November"},
        {"english": "December", "phonetic": "di-sembe", "indonesia": "Desember"},
    ],
    "Topic 2e - Time Expressions": [
        {"english": "o clock", "phonetic": "o'klok", "indonesia": "tepat dari jam 12 malam sampai 12 siang"},
        {"english": "a.m.", "phonetic": "ei-em", "indonesia": "jam 12 malam ke jam 12 siang"},
        {"english": "p.m.", "phonetic": "pi-em", "indonesia": "jam 12 siang ke jam 12 malam"},
        {"english": "quarter past", "phonetic": "kwar-ter pas", "indonesia": "lewat 15 menit"},
        {"english": "half past", "phonetic": "half-pas", "indonesia": "lewat 30 menit"},
        {"english": "quarter to", "phonetic": "kwar-ter twu", "indonesia": "kurang 15 menit"},
        {"english": "noon", "phonetic": "nun", "indonesia": "tengah hari"},
        {"english": "midday", "phonetic": "mid-dei", "indonesia": "tengah hari"},
        {"english": "opening hours", "phonetic": "opening awers", "indonesia": "jam buka"},
        {"english": "closing time", "phonetic": "klosing taim", "indonesia": "jam tutup"},
        {"english": "check in time", "phonetic": "check-in taim", "indonesia": "waktu check-in (masuk)"},
        {"english": "check out time", "phonetic": "check-aut taim", "indonesia": "waktu check-out (keluar)"},
        {"english": "1 O'clock", "phonetic": "wan o'klok", "indonesia": "jam 1"},
        {"english": "2.15", "phonetic": "twu fiftin", "indonesia": "jam 2 lewat 15"},
        {"english": "Two fifteen", "phonetic": "e kwar-ter pas twu", "indonesia": "jam 2 lewat 15"},
        {"english": "A quarter past two", "phonetic": "e kwar-ter pas twu", "indonesia": "jam 2 lewat 15"},
        {"english": "Two thirty", "phonetic": "twu ther-ti", "indonesia": "jam 2.30"},
        {"english": "A half past two", "phonetic": "e half past twu", "indonesia": "jam 2.30"},
        {"english": "Two forty five", "phonetic": "twu fo-ti faiv", "indonesia": "jam 2.45"},
        {"english": "A quarter to three", "phonetic": "e kwar-ter twu thri", "indonesia": "jam 2.45"},
    ],
    "Topic 3 - Hotel Jobs": [
        {"english": "General manager", "phonetic": "Jen-rel menejer", "indonesia": "Manajer umum"},
        {"english": "Front office manager", "phonetic": "Front ofis menejer", "indonesia": "Manajer front office"},
        {"english": "Receptionist", "phonetic": "Risep-sye-nis", "indonesia": "Resepsionis"},
        {"english": "Concierge", "phonetic": "Kon-syerj", "indonesia": "Petugas concierge"},
        {"english": "Bell boy", "phonetic": "Bel boi", "indonesia": "Petugas pembawa barang"},
        {"english": "Porter", "phonetic": "Por-ter", "indonesia": "Porter"},
        {"english": "Room attendant", "phonetic": "Rum aten-dan", "indonesia": "Petugas kebersihan kamar"},
        {"english": "Housekeeping Supervisor", "phonetic": "Haus-kiping super-vaizer", "indonesia": "Pengawas housekeeping"},
        {"english": "Laundry attendant", "phonetic": "Lon-dri atendan", "indonesia": "Petugas laundry"},
        {"english": "Waitress", "phonetic": "Wei-tres", "indonesia" : "Pramusaji"},
        {"english": "Waiter", "phonetic": "Wai-ter", "indonesia" : "Pramusaji"},
        {"english": "Bartender", "phonetic": "Bar-ten-der", "indonesia": "Bartender"},
        {"english": "Banquet manager", "phonetic": "Ben-kuet menejer", "indonesia": "Manajer Banquet"},
        {"english": "Maintenance Technician", "phonetic": "Mein-tenens tek-ni-syen", "indonesia": "Teknisi pemeliharaan"},
        {"english": "Security officer", "phonetic": "Si-kiu-riti ofiser", "indonesia": "Petugas keamanan"},
        {"english": "Spa therapist", "phonetic": "Spa terap-is", "indonesia": "Terapis spa"},
        {"english": "Lifeguard", "phonetic": "Laif-gard", "indonesia": "Penjaga kolam"},
        {"english": "Sales and Marketing Manager", "phonetic": "Seils en marketing menejer", "indonesia": "Manajer penjualan dan pemasaran"},
        {"english": "Event Coordinator", "phonetic": "Iven koor-dinetor", "indonesia": "Koordinator acara"},
    ],
    "4a - Hotel Facilities": [
        {"english": "Lobby", "phonetic": "Lobi", "indonesia": "Lobi"},
        {"english": "Reception desk", "phonetic": "Resp-syen des", "indonesia": "Meja resepsionis"},
        {"english": "Elevator", "phonetic": "Ele-vei-tor", "indonesia": "Lift"},
        {"english": "Stairs", "phonetic": "Steirs", "indonesia": "Tangga"},
        {"english": "Corridor", "phonetic": "Kori-dor", "indonesia": "Koridor"},
        {"english": "Hallway", "phonetic": "Hol-wei", "indonesia": "Lorong"},
        {"english": "Restaurant", "phonetic": "Res-to-ren", "indonesia": "Restoran"},
        {"english": "Café", "phonetic": "Ka-fei", "indonesia": "Kafe"},
        {"english": "Bar", "phonetic": "Bar", "indonesia": "Bar"},
        {"english": "Swimming pool", "phonetic": "Suiming pul", "indonesia": "Kolam renang"},
        {"english": "Spa", "phonetic": "Spa", "indonesia": "Spa"},
        {"english": "Gym", "phonetic": "Jim", "indonesia": "Pusat kebugaran"},
        {"english": "Ballroom", "phonetic": "Bol-rum", "indonesia": "Aula besar"},
        {"english": "Meeting room", "phonetic": "mi-ting rum", "indonesia": "Ruang rapat"},
        {"english": "Gift shop", "phonetic": "Gif syop", "indonesia": "Toko suvenir"},
    ],
    "4b - Prepositions of Place": [
        {"english": "In front of", "phonetic": "In front of", "indonesia": "Di depan"},
        {"english": "In the back of", "phonetic": "In de bek of", "indonesia": "Di belakang"},
        {"english": "Behind", "phonetic": "Bi-hain", "indonesia": "Di belakang"},
        {"english": "Between", "phonetic": "Bi-twin", "indonesia": "Di antara (dua benda/tempat)"},
        {"english": "Among", "phonetic": "a-mong", "indonesia": "Di antara (lebih dari dua benda/tempat)"},
        {"english": "Next to", "phonetic": "Neks tu", "indonesia": "Di sebelah/ di samping"},
        {"english": "Beside", "phonetic": "Bi-said", "indonesia": "Di samping"},
        {"english": "Near", "phonetic": "Nir", "indonesia": "Dekat"},
        {"english": "At the corner", "phonetic": "Et de kor-ner", "indonesia": "Di sudut/di pojok"},
        {"english": "Turn left", "phonetic": "Tern lef", "indonesia": "Belok kiri"},
        {"english": "Turn right", "phonetic": "Tern rait", "indonesia": "Belok kanan"},
        {"english": "Go straight", "phonetic": "Go strait", "indonesia": "Jalan lurus"},
        {"english": "Far from", "phonetic": "Far from", "indonesia": "Jauh dari"},
    ],
    "4c - Places": [
        {"english": "Beach", "phonetic": "Bich", "indonesia": "Pantai"},
        {"english": "Museum", "phonetic": "myu-zi-em", "indonesia": "Museum"},
        {"english": "Art gallery", "phonetic": "art gal-e-ri", "indonesia": "Galeri seni"},
        {"english": "Shopping mall", "phonetic": "syap-ping mol", "indonesia": "Pusat perbelanjaan"},
        {"english": "Market", "phonetic": "mar-ket", "indonesia": "Pasar"},
        {"english": "Park", "phonetic": "Park", "indonesia": "Taman kota"},
        {"english": "Zoo", "phonetic": "Zu", "indonesia": "Kebun binatang"},
        {"english": "Aquarium", "phonetic": "a-kwe-ri-em", "indonesia": "Akuarium"},
        {"english": "Theme park", "phonetic": "tim park", "indonesia": "Taman hiburan"},
        {"english": "Historical site", "phonetic": "his-to-ri-kel sait", "indonesia": "Situs bersejarah"},
        {"english": "Monument", "phonetic": "mo-nyu-ment", "indonesia": "Monumen"},
        {"english": "Church", "phonetic": "cerch", "indonesia": "Gereja"},
        {"english": "Mosque", "phonetic": "Mosk", "indonesia": "Masjid"},
        {"english": "Temple", "phonetic": "tem-pel", "indonesia": "Kuil / Pura"},
        {"english": "Cinema", "phonetic": "si-ne-ma", "indonesia": "Bioskop"},
        {"english": "Stadium", "phonetic": "ste-di-em", "indonesia": "Stadion"},
        {"english": "Harbor", "phonetic": "har-bor", "indonesia": "Pelabuhan"},
        {"english": "River", "phonetic": "ri-ver", "indonesia": "Sungai"},
        {"english": "Lake", "phonetic": "Leik", "indonesia": "Danau"},
        {"english": "Mountain", "phonetic": "moun-ten", "indonesia": "Gunung"},
        {"english": "Waterfall", "phonetic": "wo-ter-fol", "indonesia": "Air terjun"},
        {"english": "Botanical garden", "phonetic": "bo-ta-ni-kel gar-den", "indonesia": "Kebun raya"},
        {"english": "Traditional village", "phonetic": "tre-di-syo-nel vil-ij", "indonesia": "Desa tradisional"},
        {"english": "Handicraft center", "phonetic": "han-di-kraft sen-ter", "indonesia": "Pusat kerajinan tangan"},
        {"english": "Cultural center", "phonetic": "kal-chur-ei sen-ter", "indonesia": "Pusat kebudayaan"},
    ],
    "4d - Giving Directions": [
        {"english": "Go ahead", "phonetic": "go e-hed", "indonesia": "Jalan lurus"},
        {"english": "Go along", "phonetic": "go e-long", "indonesia": "Menyusuri / mengikuti"},
        {"english": "Turn left", "phonetic": "tern lef", "indonesia": "Belok kiri"},
        {"english": "Turn right", "phonetic": "tern rait", "indonesia": "Belok kanan"},
        {"english": "Go past", "phonetic": "go past", "indonesia": "Lewati (melewati)"},
        {"english": "Cross the street", "phonetic": "kros de strit", "indonesia": "Menyeberang jalan"},
        {"english": "At the corner", "phonetic": "at de kor-ner", "indonesia": "Di sudut jalan"},
        {"english": "At the intersection", "phonetic": "at de in-ter-sek-syen", "indonesia": "Di persimpangan"},
        {"english": "Near", "phonetic": "Nir", "indonesia": "Dekat"},
        {"english": "Next to", "phonetic": "Neks tu", "indonesia": "Di sebelah"},
        {"english": "Opposite", "phonetic": "o-po-sit", "indonesia": "Di seberang"},
        {"english": "In front of", "phonetic": "in front of", "indonesia": "Di depan"},
        {"english": "Behind", "phonetic": "bi-haind", "indonesia": "Di belakang"},
        {"english": "Cross the road", "phonetic": "kros de rod", "indonesia": "Seberangi jalan"},
        {"english": "Go up the street", "phonetic": "go ap de strit", "indonesia": "Naik (jalan menanjak)"},
        {"english": "Go down the street", "phonetic": "go daun de strit", "indonesia": "Turun (jalan menurun)"},
        {"english": "Around the corner", "phonetic": "e-raund de kor-ner", "indonesia": "Di sekitar sudut jalan"},
        {"english": "At the traffic light", "phonetic": "at de tra-fik lait", "indonesia": "Di lampu lalu lintas"},
        {"english": "At the end of", "phonetic": "at de end ov", "indonesia": "Di ujung"},
        {"english": "Take the first left", "phonetic": "teik de fers lef", "indonesia": "Ambil belokan kiri pertama"},
        {"english": "Take the second right", "phonetic": "teik de se-kend rait", "indonesia": "Ambil belokan kanan kedua"},
        {"english": "Across from", "phonetic": "e-kros from", "indonesia": "Tepat di seberang"},
    ],
    "5 - Reservation & Booking": [
        {"english": "Reservation", "phonetic": "rez-er-vey-syen", "indonesia": "Pemesanan"},
        {"english": "Booking", "phonetic": "buk-ing", "indonesia": "Pemesanan / Booking"},
        {"english": "Check in", "phonetic": "cek-in", "indonesia": "Proses masuk hotel"},
        {"english": "Check out", "phonetic": "cek-aut", "indonesia": "Proses keluar hotel"},
        {"english": "Confirmation", "phonetic": "kon-fer-mey-syen", "indonesia": "Konfirmasi"},
        {"english": "Availability", "phonetic": "e-vei-le-bil-i-ti", "indonesia": "Ketersediaan"},
        {"english": "Single room", "phonetic": "sing-gal rum", "indonesia": "Kamar untuk satu orang"},
        {"english": "Double room", "phonetic": "dab-el rum", "indonesia": "Kamar untuk dua orang (1 ranjang)"},
        {"english": "Twin room", "phonetic": "twin rum", "indonesia": "Kamar dengan 2 ranjang terpisah"},
        {"english": "Suite", "phonetic": "suit (dibaca: swit)", "indonesia": "Kamar mewah / lebih besar"},
        {"english": "Deposit", "phonetic": "di-po-zit", "indonesia": "Uang muka / jaminan"},
        {"english": "Cancellation", "phonetic": "kan-se-lei-syen", "indonesia": "Pembatalan"},
        {"english": "Non refundable", "phonetic": "non-ri-fan-de-bal", "indonesia": "Tidak bisa dikembalikan (uang)"},
        {"english": "Payment method", "phonetic": "pei-ment met-had", "indonesia": "Metode pembayaran"},
        {"english": "Credit card", "phonetic": "kred-it kard", "indonesia": "Kartu kredit"},
        {"english": "Guest", "phonetic": "gest", "indonesia": "Tamu"},
        {"english": "Reception", "phonetic": "ri-sep-syen", "indonesia": "Resepsionis / meja depan"},
        {"english": "Reservation number", "phonetic": "rez-er-vey-syen nam-ber", "indonesia": "Nomor pemesanan"},
        {"english": "Early check in", "phonetic": "er-li cek-in", "indonesia": "Masuk lebih awal"},
        {"english": "Late check out", "phonetic": "leit cek-aut", "indonesia": "Keluar lebih lambat"},
    ],
    "6 - Hotel Payments & Policies": [
        {"english": "Bill", "phonetic": "Bil", "indonesia": "Tagihan"},
        {"english": "Invoice", "phonetic": "in-vois", "indonesia": "Tagihan"},
        {"english": "Receipt", "phonetic": "Ri-sit", "indonesia": "Tanda terima"},
        {"english": "Payment method", "phonetic": "Pei-men met-hod", "indonesia": "Metode pembayaran"},
        {"english": "Cash", "phonetic": "Kesh", "indonesia": "Uang tunai"},
        {"english": "Check card", "phonetic": "Chek-kard", "indonesia": "Kartu debit"},
        {"english": "Feedback Form", "phonetic": "Fid-bek form", "indonesia": "Formulir masukan"},
        {"english": "Thank you for staying", "phonetic": "Thenk-yu for stei-ing", "indonesia": "Terima kasih telah menginap"},
        {"english": "Check in time", "phonetic": "Cek-in taim", "indonesia": "Waktu check-in"},
        {"english": "Check out time", "phonetic": "Cek-aut taim", "indonesia": "Waktu check-out"},
        {"english": "Early check in", "phonetic": "Er-li cek-in", "indonesia": "Check-in lebih awal"},
        {"english": "Late check out", "phonetic": "Leit cek-aut", "indonesia": "Check-out lebih lambat"},
        {"english": "Luggage", "phonetic": "Lag-gej", "indonesia": "Bagasi"},
        {"english": "Bellboy", "phonetic": "Bel-boi", "indonesia": "Petugas pengantar barang"},
        {"english": "Concierge", "phonetic": "Kon-si-erj", "indonesia": "Petugas layanan tamu"},
        {"english": "Front desk", "phonetic": "Fran-desk", "indonesia": "Resepsionis"},
        {"english": "Booking reference number", "phonetic": "Buk-ing re-fe-ren-si nam-ber", "indonesia": "Nomor referensi pemesanan"},
        {"english": "Room rate", "phonetic": "Rum reit", "indonesia": "Tarif kamar"},
        {"english": "Extension night", "phonetic": "Eks-ten-syen nait", "indonesia": "Perpanjangan malam menginap"},
        {"english": "Cancellation policy", "phonetic": "Kan-se-lei-syen po-li-si", "indonesia": "Kebijakan pembatalan"},
        {"english": "No show", "phonetic": "Nou-syau", "indonesia": "Tamu tidak hadir"},
        {"english": "Upgrade room", "phonetic": "Ap-greid rum", "indonesia": "Peningkatan tipe kamar"},
    ],
    "7a - Hotel Facilities & Services": [
        {"english": "Gym", "phonetic": "jim", "indonesia": "Pusat kebugaran"},
        {"english": "Spa", "phonetic": "spa", "indonesia": "Spa / Tempat relaksasi"},
        {"english": "Business center", "phonetic": "biz-nes sen-ter", "indonesia": "Pusat bisnis"},
        {"english": "Shuttle service", "phonetic": "syatel ser-vis", "indonesia": "Layanan antar-jemput"},
        {"english": "24 hour reception", "phonetic": "twenti for awr ri-sep-syen", "indonesia": "Resepsionis 24 jam"},
        {"english": "Room service", "phonetic": "rum ser-vis", "indonesia": "Layanan kamar"},
        {"english": "Swimming pool", "phonetic": "swim-ming pul", "indonesia": "Kolam renang"},
        {"english": "Restaurant", "phonetic": "res-to-ran(t)", "indonesia": "Restoran"},
        {"english": "Bar", "phonetic": "bar", "indonesia": "Bar"},
        {"english": "Conference room", "phonetic": "kon-frens rum", "indonesia": "Ruang konferensi"},
        {"english": "Parking area", "phonetic": "par-king e-ria", "indonesia": "Area parkir"},
        {"english": "Complimentary breakfast", "phonetic": "kom-pli-men-ta-ri brek-fest", "indonesia": "Sarapan gratis"},
        {"english": "Wi-fi access", "phonetic": "wai-fai ak-ses", "indonesia": "Akses wi-fi"},
        {"english": "Garden", "phonetic": "gar-den", "indonesia": "Taman"},
        {"english": "Lounge", "phonetic": "launj", "indonesia": "Ruang santai"},
        {"english": "Playground", "phonetic": "plei-grouwnd", "indonesia": "Taman bermain anak"},
        {"english": "Elevator", "phonetic": "e-le-ve-tor", "indonesia": "Lift"},
        {"english": "Banquet hall", "phonetic": "ban-kuet hol", "indonesia": "Aula / Gedung perjamuan"},
        {"english": "Lobby", "phonetic": "lo-bi", "indonesia": "Lobi"},
        {"english": "Front desk", "phonetic": "frant desk", "indonesia": "Meja resepsionis"},
        {"english": "Gift shop", "phonetic": "gift shop", "indonesia": "Toko cenderamata"},
        {"english": "Laundry service", "phonetic": "lon-dri ser-vis", "indonesia": "Layanan binatu/cuci"},
        {"english": "Valet parking", "phonetic": "va-lei par-king", "indonesia": "Parkir valet"},
        {"english": "ATM", "phonetic": "ei-ti-em", "indonesia": "Mesin ATM"},
        {"english": "Kids club", "phonetic": "kids klab", "indonesia": "Klub anak-anak"},
        {"english": "Rooftop terrace", "phonetic": "ruf-top te-res", "indonesia": "Teras atap"},
        {"english": "Karaoke room", "phonetic": "ka-ra-o-ke rum", "indonesia": "Ruang karaoke"},
        {"english": "Cinema room", "phonetic": "si-ne-ma rum", "indonesia": "Ruang bioskop mini"},
    ],
    "7b - Room Descriptions": [
        {"english": "Spacious", "phonetic": "Spey-syus", "indonesia": "Luas"},
        {"english": "Comfortable", "phonetic": "Kam-fer-tebel", "indonesia": "Nyaman"},
        {"english": "Luxurious", "phonetic": "Lug-syu-rius", "indonesia": "Mewah"},
        {"english": "Modern", "phonetic": "Mo-dern", "indonesia": "Modern"},
        {"english": "Elegant", "phonetic": "elegan", "indonesia": "Elegan"},
        {"english": "Cozy", "phonetic": "Kou-zi", "indonesia": "Hangat dan nyaman"},
        {"english": "Clean", "phonetic": "klin", "indonesia": "Bersih"},
        {"english": "Well equipped", "phonetic": "Wel-i-kwip", "indonesia": "Dilengkapi dengan baik"},
        {"english": "Convenient", "phonetic": "Kon-vini-en", "indonesia": "Praktis/mudah diakses"},
        {"english": "Private", "phonetic": "Prai-vet", "indonesia": "Pribadi"},
        {"english": "Quiet", "phonetic": "Kwai-et", "indonesia": "Tenang"},
        {"english": "Bright", "phonetic": "brait", "indonesia": "Terang"},
        {"english": "Affordable", "phonetic": "Afor-dabel", "indonesia": "Terjangkau"},
        {"english": "Impressive", "phonetic": "im-presif", "indonesia": "Mengesankan"},
        {"english": "Relaxing", "phonetic": "ri-lek-sing", "indonesia": "Menyenangkan"},
        {"english": "Family friendly", "phonetic": "Fae-mili fren-li", "indonesia": "Ramah untuk keluarga"},
        {"english": "Scenic", "phonetic": "sinik", "indonesia": "Indah (pemandangan)"},
        {"english": "Accessible", "phonetic": "Akses-sebel", "indonesia": "Mudah diakses"},
    ],
    "8a - Restaurant & Dining": [
        {"english": "Menu", "phonetic": "me-nyu", "indonesia": "Daftar makanan"},
        {"english": "Appetizer", "phonetic": "e-pe-tai-zer", "indonesia": "Hidangan pembuka"},
        {"english": "Main course", "phonetic": "mein kors", "indonesia": "Hidangan utama"},
        {"english": "Side dish", "phonetic": "said disy", "indonesia": "Hidangan pendamping"},
        {"english": "Dessert", "phonetic": "di-zert", "indonesia": "Hidangan penutup"},
        {"english": "Beverage", "phonetic": "be-ve-rej", "indonesia": "Minuman"},
        {"english": "Soft drink", "phonetic": "soft dringk", "indonesia": "Minuman ringan (soda)"},
        {"english": "Mineral water", "phonetic": "mi-ne-ral woter", "indonesia": "Air mineral"},
        {"english": "Sparkling water", "phonetic": "spark-ling woter", "indonesia": "Air soda"},
        {"english": "Coffee", "phonetic": "kofi", "indonesia": "Kopi"},
        {"english": "Tea", "phonetic": "ti", "indonesia": "Teh"},
        {"english": "Juice", "phonetic": "jus", "indonesia": "Jus"},
        {"english": "Wine", "phonetic": "wain", "indonesia": "Anggur"},
        {"english": "Beer", "phonetic": "bir", "indonesia": "Bir"},
        {"english": "Cocktail", "phonetic": "kok-teyl", "indonesia": "Koktail"},
        {"english": "Mocktail", "phonetic": "mok-teyl", "indonesia": "Minuman non-alkohol"},
        {"english": "Buffet", "phonetic": "bu-fe", "indonesia": "Hidangan prasmanan"},
        {"english": "À la carte", "phonetic": "a la kart", "indonesia": "Pesan per porsi/menu"},
        {"english": "Room service tray", "phonetic": "rum ser-vis trey", "indonesia": "Baki layanan kamar"},
        {"english": "Waitress", "phonetic": "wei-tres", "indonesia": "Pramusaji wanita"},
        {"english": "Waiter", "phonetic": "wai-ter", "indonesia": "Pramusaji pria"},
        {"english": "Bartender", "phonetic": "bar-ten-der", "indonesia": "Peracik minuman di bar"},
        {"english": "Chef", "phonetic": "sef", "indonesia": "Koki"},
        {"english": "Order", "phonetic": "or-der", "indonesia": "Pesanan"},
        {"english": "Take order", "phonetic": "teyk or-der", "indonesia": "Menerima pesanan"},
        {"english": "Place an order", "phonetic": "pleys an or-der", "indonesia": "Memesan makanan/minuman"},
        {"english": "Bill", "phonetic": "bil", "indonesia": "Tagihan"},
        {"english": "Tip", "phonetic": "tip", "indonesia": "Uang tip"},
        {"english": "Table setting", "phonetic": "tey-bel se-ting", "indonesia": "Tata meja"},
        {"english": "Reservation", "phonetic": "rezervesyen teybel", "indonesia": "Reservasi meja"},
        {"english": "Occupied table", "phonetic": "o-kyu-pai-d te-bel", "indonesia": "Meja terisi"},
        {"english": "Available table", "phonetic": "e-vei-le-bel te-bel", "indonesia": "Meja tersedia"},
        {"english": "Napkin", "phonetic": "nep-kin", "indonesia": "Serbet"},
        {"english": "Cutlery", "phonetic": "kat-ler-ri", "indonesia": "Alat makan (sendok/garpu)"},
        {"english": "Plate", "phonetic": "pleyt", "indonesia": "Piring"},
        {"english": "Bowl", "phonetic": "boul", "indonesia": "Mangkuk"},
        {"english": "Glass", "phonetic": "glas", "indonesia": "Gelas"},
        {"english": "Spoon", "phonetic": "spun", "indonesia": "Sendok"},
        {"english": "Fork", "phonetic": "fork", "indonesia": "Garpu"},
        {"english": "Knife", "phonetic": "naif", "indonesia": "Pisau"},
        {"english": "Tray", "phonetic": "trey", "indonesia": "Baki"},
        {"english": "Serving", "phonetic": "ser-ving", "indonesia": "Penyajian"},
        {"english": "Portion", "phonetic": "por-syen", "indonesia": "Porsi"},
        {"english": "Takeaway", "phonetic": "teyk-a-wey", "indonesia": "Dibungkus"},
        {"english": "Special request", "phonetic": "spesyel rikwest", "indonesia": "Permintaan khusus"},
        {"english": "Allergy", "phonetic": "a-ler-ji", "indonesia": "Alergi"},
        {"english": "Vegetarian option", "phonetic": "ve-je-te-ri-an op-syen", "indonesia": "Menu vegetarian"},
        {"english": "Halal food", "phonetic": "ha-lal fud", "indonesia": "Makanan halal"},
        {"english": "Non smoking area", "phonetic": "non-smou-king e-ria", "indonesia": "Area bebas rokok"}
    ],

    "8b - Food & Taste": [
        {"english": "Delicious", "phonetic": "di-lis-syus", "indonesia": "Lezat"},
        {"english": "Tasty", "phonetic": "teys-ti", "indonesia": "Enak"},
        {"english": "Fresh", "phonetic": "fresh", "indonesia": "Segar"},
        {"english": "Spicy", "phonetic": "spay-si", "indonesia": "Pedas"},
        {"english": "Sweet", "phonetic": "swit", "indonesia": "Manis"},
        {"english": "Bitter", "phonetic": "bi-ter", "indonesia": "Pahit"},
        {"english": "Sour", "phonetic": "sau-er", "indonesia": "Asam"},
        {"english": "Salty", "phonetic": "sol-ti", "indonesia": "Asin"},
        {"english": "Juicy", "phonetic": "ju-si", "indonesia": "Berair / juicy"},
        {"english": "Crispy", "phonetic": "kris-pi", "indonesia": "Renyah / garing"},
        {"english": "Tender", "phonetic": "ten-der", "indonesia": "Empuk (untuk daging)"},
        {"english": "Chewy", "phonetic": "chu-wi", "indonesia": "Kenyal"},
        {"english": "Creamy", "phonetic": "kri-mi", "indonesia": "Lembut, berkrim"},
        {"english": "Savoury", "phonetic": "sey-vo-ri", "indonesia": "Gurih"},
        {"english": "Bland", "phonetic": "blend", "indonesia": "Hambar"},
        {"english": "Hot", "phonetic": "hot", "indonesia": "Panas"},
        {"english": "Cold", "phonetic": "kold", "indonesia": "Dingin"},
        {"english": "Fizzy", "phonetic": "fi-zi", "indonesia": "Bersoda"},
        {"english": "Strong", "phonetic": "strong", "indonesia": "Kuat (rasa)"},
        {"english": "Light", "phonetic": "lait", "indonesia": "Ringan (rasa)"},
        {"english": "Rich", "phonetic": "rich", "indonesia": "Kaya rasa"},
        {"english": "Flavorful", "phonetic": "fley-ver-ful", "indonesia": "Penuh rasa"},
        {"english": "Aromatic", "phonetic": "a-ro-ma-tik", "indonesia": "Harum"}
    ],

    "9 - Housekeeping": [
        {"english": "Housekeeping", "phonetic": "Haus-ki-ping", "indonesia": "Tata graha (bagian kebersihan hotel)"},
        {"english": "Room Service", "phonetic": "Rum ser-vis", "indonesia": "Layanan kamar"},
        {"english": "Laundry", "phonetic": "Lon-dri", "indonesia": "Binatu / Cuci pakaian"},
        {"english": "Linen", "phonetic": "Li-nen", "indonesia": "Kain (seprai, sarung bantal, dsb.)"},
        {"english": "Pillow", "phonetic": "Pi-lo", "indonesia": "Bantal"},
        {"english": "Blanket", "phonetic": "Bleng-ket", "indonesia": "Selimut"},
        {"english": "Bed Sheet", "phonetic": "Bed-syit", "indonesia": "Seprai"},
        {"english": "Towel", "phonetic": "Tau-el", "indonesia": "Handuk"},
        {"english": "Bathrobe", "phonetic": "Bath-rob", "indonesia": "Jubah mandi"},
        {"english": "Slippers", "phonetic": "Sli-pers", "indonesia": "Sandal kamar"},
        {"english": "Mattress", "phonetic": "Met-res", "indonesia": "Kasur"},
        {"english": "Quilt", "phonetic": "Kwil", "indonesia": "Selimut tebal"},
        {"english": "Air Conditioner", "phonetic": "E-kon-di-syener", "indonesia": "Pendingin ruangan"},
        {"english": "Curtain", "phonetic": "Ker-ten", "indonesia": "Gorden"},
        {"english": "Carpet", "phonetic": "Ker-pet", "indonesia": "Karpet"},
        {"english": "Wardrobe", "phonetic": "Word-rob", "indonesia": "Lemari pakaian"},
        {"english": "Drawer", "phonetic": "Dro-wor", "indonesia": "Laci"},
        {"english": "Mirror", "phonetic": "Mir-or", "indonesia": "Cermin"},
        {"english": "Hanger", "phonetic": "Heng-ger", "indonesia": "Gantungan baju"},
        {"english": "Amenities", "phonetic": "e-me-ni-tis", "indonesia": "Fasilitas pelengkap"},
        {"english": "Matches", "phonetic": "Me-tshes", "indonesia": "Korek/batang korek api"},
        {"english": "Soap", "phonetic": "Sop", "indonesia": "Sabun"},
        {"english": "Shampoo", "phonetic": "Syam-pu", "indonesia": "Sampo"},
        {"english": "Toothbrush", "phonetic": "Tut-brisy", "indonesia": "Sikat gigi"},
        {"english": "Toothpaste", "phonetic": "Tut-peist", "indonesia": "Pasta gigi"},
        {"english": "Lotion", "phonetic": "Lo-syen", "indonesia": "Losion"},
        {"english": "Hairdryer", "phonetic": "Her-dray-yer", "indonesia": "Pengering rambut"},
        {"english": "Dustpan", "phonetic": "Das-pen", "indonesia": "Serokan sampah"},
        {"english": "Vacuum Cleaner", "phonetic": "Ve-kiuim Kli-ner", "indonesia": "Penyedot debu"},
        {"english": "Mop", "phonetic": "Mop", "indonesia": "Pel"},
        {"english": "Broom", "phonetic": "Brum", "indonesia": "Sapu"},
        {"english": "Room Key", "phonetic": "Rum-ki", "indonesia": "Kunci kamar"},
        {"english": "Key Card", "phonetic": "Ki-kard", "indonesia": "Kartu kunci"},
        {"english": "Minibar", "phonetic": "Mi-ni-bar", "indonesia": "Minibar"},
        {"english": "Safe Deposit Box", "phonetic": "Seif de-po-zit boks", "indonesia": "Brankas"},
        {"english": "Telephone", "phonetic": "Tel-fon", "indonesia": "Telepon"},
        {"english": "Television", "phonetic": "Tel-e-vi-syen", "indonesia": "Televisi"},
        {"english": "Remote control", "phonetic": "Ri-mot kon-trol", "indonesia": "Remote control"},
        {"english": "Lamp", "phonetic": "Lemp", "indonesia": "Lampu"},
        {"english": "Light Switch", "phonetic": "Lait swits", "indonesia": "Sakelar lampu"},
        {"english": "Fridge", "phonetic": "Fri-j", "indonesia": "Kulkas"},
        {"english": "Kettle", "phonetic": "Ke-tel", "indonesia": "Teko listrik"},
        {"english": "Coffee Maker", "phonetic": "Ko-fi mey-ker", "indonesia": "Mesin pembuat kopi"},
        {"english": "Iron", "phonetic": "Ay-ron", "indonesia": "Setrika"},
        {"english": "Ironing Board", "phonetic": "Ay-ron-ing bord", "indonesia": "Meja setrika"}
    ],

    "10 - Complaints & Solutions": [
        {"english": "Sorry for the inconvenience", "phonetic": "Sory for di in-kan-fi-niens", "indonesia": "Maaf atas ketidaknyamanannya"},
        {"english": "Apologize", "phonetic": "a-po-lo-jaiz", "indonesia": "Meminta maaf"},
        {"english": "Complaint", "phonetic": "kom-pleint", "indonesia": "Keluhan"},
        {"english": "Issue", "phonetic": "I-syu", "indonesia": "Masalah"},
        {"english": "Inconvenience", "phonetic": "in-kan-vi-ni-ens", "indonesia": "Ketidaknyamanan"},
        {"english": "Misunderstanding", "phonetic": "mis-an-der-sten-ding", "indonesia": "Kesalahpahaman"},
        {"english": "Dissatisfied", "phonetic": "dis-sa-tis-faied", "indonesia": "Tidak puas"},
        {"english": "Urgent", "phonetic": "er-jent", "indonesia": "Mendesak"},
        {"english": "Fixing", "phonetic": "Fik-sing", "indonesia": "Memperbaiki"},
        {"english": "Solution", "phonetic": "so-lu-syen", "indonesia": "Solusi"},
        {"english": "Compensation", "phonetic": "kom-pen-sei-syen", "indonesia": "Kompensasi / ganti rugi"},
        {"english": "Refund", "phonetic": "ri-fand", "indonesia": "Pengembalian uang"},
        {"english": "Replace", "phonetic": "ri-pleis", "indonesia": "Mengganti"},
        {"english": "Delay", "phonetic": "di-lei", "indonesia": "Keterlambatan"},
        {"english": "Policy", "phonetic": "po-li-si", "indonesia": "Kebijakan"},
        {"english": "Explanation", "phonetic": "eks-ple-nei-syen", "indonesia": "Penjelasan"},
        {"english": "Clarify", "phonetic": "kle-ri-fai", "indonesia": "Menjelaskan / memperjelas"},
        {"english": "Escalate", "phonetic": "es-ke-leit", "indonesia": "Meningkatkan ke atasan"},
        {"english": "Feedback", "phonetic": "fid-bek", "indonesia": "Masukan / tanggapan"},
        {"english": "Assistance", "phonetic": "e-sis-tens", "indonesia": "Bantuan"},
        {"english": "Guarantee", "phonetic": "ge-ren-ti", "indonesia": "Jaminan"}
    ],
    "11 - Handling Reservation": [
        {"english": "Reservation", "phonetic": "re-zer-vei-syen", "indonesia": "Pemesanan"},
        {"english": "Book a room", "phonetic": "buk a rum", "indonesia": "Memesan kamar"},
        {"english": "Confirm", "phonetic": "kon-ferm", "indonesia": "Mengonfirmasi"},
        {"english": "Availability", "phonetic": "a-vei-la-bi-li-ti", "indonesia": "Ketersediaan"},
        {"english": "Fully booked", "phonetic": "fu-li bukd", "indonesia": "Sudah penuh"},
        {"english": "Check availability", "phonetic": "cek a-vei-la-bi-li-ti", "indonesia": "Cek ketersediaan"},
        {"english": "Cancellation", "phonetic": "kan-se-lei-syen", "indonesia": "Pembatalan"},
        {"english": "Deposit", "phonetic": "di-po-zit", "indonesia": "Uang muka / deposit"},
        {"english": "Advance payment", "phonetic": "ad-vans pei-ment", "indonesia": "Pembayaran di muka"},
        {"english": "Guarantee", "phonetic": "ge-ren-ti", "indonesia": "Jaminan"},
        {"english": "Credit card", "phonetic": "kre-dit kard", "indonesia": "Kartu kredit"},
        {"english": "Check in date", "phonetic": "cek in deit", "indonesia": "Tanggal masuk"},
        {"english": "Check out date", "phonetic": "cek aut deit", "indonesia": "Tanggal keluar"},
        {"english": "Special request", "phonetic": "spe-syel ri-kwest", "indonesia": "Permintaan khusus"},
        {"english": "Single room", "phonetic": "sing-gel rum", "indonesia": "Kamar tunggal"},
        {"english": "Double room", "phonetic": "da-bel rum", "indonesia": "Kamar ganda"},
        {"english": "Suite", "phonetic": "swit", "indonesia": "Kamar suite"},
        {"english": "Duration of stay", "phonetic": "du-rei-syen of stei", "indonesia": "Lama menginap"},
        {"english": "Reference number", "phonetic": "re-fe-rens nam-ber", "indonesia": "Nomor referensi"},
        {"english": "Walk in guest", "phonetic": "wok in gest", "indonesia": "Tamu langsung tanpa reservasi"}
    ],

"12 - Tourism Information": [
        {"english": "Tourist attraction", "phonetic": "tu-rist at-rak-syen", "indonesia": "Tempat wisata"},
        {"english": "Sightseeing", "phonetic": "sait-sii-ing", "indonesia": "Jalan-jalan melihat pemandangan"},
        {"english": "Destination", "phonetic": "des-ti-nei-syen", "indonesia": "Tujuan wisata"},
        {"english": "Tour guide", "phonetic": "tur gaid", "indonesia": "Pemandu wisata"},
        {"english": "Excursion", "phonetic": "eks-ker-syen", "indonesia": "Karya wisata / tamasya"},
        {"english": "Map", "phonetic": "map", "indonesia": "Peta"},
        {"english": "Nearby", "phonetic": "nir-bai", "indonesia": "Di dekat"},
        {"english": "Local culture", "phonetic": "lo-kel kal-cer", "indonesia": "Budaya lokal"},
        {"english": "Traditional market", "phonetic": "tre-di-sye-nel mar-ket", "indonesia": "Pasar tradisional"},
        {"english": "Souvenir", "phonetic": "su-ve-nir", "indonesia": "Oleh-oleh"},
        {"english": "Transportation", "phonetic": "trans-por-tei-syen", "indonesia": "Transportasi"},
        {"english": "Heritage", "phonetic": "he-ri-tej", "indonesia": "Warisan budaya"},
        {"english": "Historical site", "phonetic": "his-to-ri-kel sait", "indonesia": "Situs bersejarah"},
        {"english": "Museum", "phonetic": "myu-zi-em", "indonesia": "Museum"},
        {"english": "Temple", "phonetic": "tem-pel", "indonesia": "Kuil / candi"},
        {"english": "Beach", "phonetic": "bich", "indonesia": "Pantai"},
        {"english": "Mountain", "phonetic": "maun-ten", "indonesia": "Gunung"},
        {"english": "National park", "phonetic": "na-sye-nel park", "indonesia": "Taman nasional"},
        {"english": "Entrance fee", "phonetic": "en-trens fi", "indonesia": "Tiket masuk"},
        {"english": "Opening hours", "phonetic": "o-pen-ing au-ers", "indonesia": "Jam buka"}
    ],

"13 - Telephone Handling": [
        {"english": "Answer the phone", "phonetic": "an-ser de fon", "indonesia": "Menjawab telepon"},
        {"english": "Hold the line", "phonetic": "hold de lain", "indonesia": "Mohon tunggu"},
        {"english": "Transfer the call", "phonetic": "trans-fer de kol", "indonesia": "Meneruskan panggilan"},
        {"english": "Extension number", "phonetic": "eks-ten-syen nam-ber", "indonesia": "Nomor sambungan"},
        {"english": "Operator", "phonetic": "o-pe-rei-tor", "indonesia": "Operator"},
        {"english": "Voicemail", "phonetic": "vois-mel", "indonesia": "Pesan suara"},
        {"english": "Busy tone", "phonetic": "bi-zi ton", "indonesia": "Nada sibuk"},
        {"english": "Dial", "phonetic": "dai-el", "indonesia": "Memutar nomor telepon"},
        {"english": "Pick up", "phonetic": "pik ap", "indonesia": "Mengangkat telepon"},
        {"english": "Hang up", "phonetic": "heng ap", "indonesia": "Menutup telepon"},
        {"english": "Long distance call", "phonetic": "long dis-tens kol", "indonesia": "Telepon jarak jauh"},
        {"english": "Collect call", "phonetic": "ko-lekt kol", "indonesia": "Telepon dibayar penerima"},
        {"english": "International call", "phonetic": "in-ter-na-sye-nel kol", "indonesia": "Telepon internasional"},
        {"english": "Wrong number", "phonetic": "rong nam-ber", "indonesia": "Nomor salah"},
        {"english": "Directory", "phonetic": "di-rek-to-ri", "indonesia": "Daftar nomor telepon"},
        {"english": "Receptionist", "phonetic": "ri-sep-sye-nist", "indonesia": "Resepsionis"},
        {"english": "Take a message", "phonetic": "teik a me-sej", "indonesia": "Mencatat pesan"},
        {"english": "Leave a message", "phonetic": "liv a me-sej", "indonesia": "Meninggalkan pesan"},
        {"english": "Call back", "phonetic": "kol bek", "indonesia": "Menelpon kembali"},
        {"english": "Switchboard", "phonetic": "swic-bord", "indonesia": "Papan sambungan telepon"}
    ],

"14 - Airport & Travel": [
        {"english": "Airport", "phonetic": "er-port", "indonesia": "Bandara"},
        {"english": "Flight", "phonetic": "flait", "indonesia": "Penerbangan"},
        {"english": "Airline", "phonetic": "er-lain", "indonesia": "Maskapai"},
        {"english": "Boarding pass", "phonetic": "bor-ding pas", "indonesia": "Kartu naik pesawat"},
        {"english": "Check in counter", "phonetic": "cek in kaun-ter", "indonesia": "Loket check-in"},
        {"english": "Gate", "phonetic": "geit", "indonesia": "Pintu keberangkatan"},
        {"english": "Departure", "phonetic": "di-par-cer", "indonesia": "Keberangkatan"},
        {"english": "Arrival", "phonetic": "a-rai-val", "indonesia": "Kedatangan"},
        {"english": "Customs", "phonetic": "kas-tems", "indonesia": "Bea cukai"},
        {"english": "Immigration", "phonetic": "i-mi-grei-syen", "indonesia": "Imigrasi"},
        {"english": "Baggage claim", "phonetic": "ba-gez kleim", "indonesia": "Pengambilan bagasi"},
        {"english": "Delayed flight", "phonetic": "di-leid flait", "indonesia": "Penerbangan tertunda"},
        {"english": "Cancelled flight", "phonetic": "kan-seld flait", "indonesia": "Penerbangan dibatalkan"},
        {"english": "On time", "phonetic": "on taim", "indonesia": "Tepat waktu"},
        {"english": "Boarding time", "phonetic": "bor-ding taim", "indonesia": "Waktu naik pesawat"},
        {"english": "Transit", "phonetic": "tran-sit", "indonesia": "Transit"},
        {"english": "Layover", "phonetic": "lei-o-ver", "indonesia": "Singgah sementara"},
        {"english": "Security check", "phonetic": "se-kyu-ri-ti cek", "indonesia": "Pemeriksaan keamanan"},
        {"english": "Runway", "phonetic": "ran-wei", "indonesia": "Landasan pacu"},
        {"english": "Flight attendant", "phonetic": "flait a-ten-dent", "indonesia": "Pramugari / pramugara"}
    ],

"15 - Hotel Facilities": [
        {"english": "Swimming pool", "phonetic": "swim-ing pul", "indonesia": "Kolam renang"},
        {"english": "Gym", "phonetic": "jim", "indonesia": "Pusat kebugaran"},
        {"english": "Spa", "phonetic": "spa", "indonesia": "Pusat spa"},
        {"english": "Restaurant", "phonetic": "res-tro-rent", "indonesia": "Restoran"},
        {"english": "Café", "phonetic": "ka-fei", "indonesia": "Kafe"},
        {"english": "Bar", "phonetic": "bar", "indonesia": "Bar"},
        {"english": "Lounge", "phonetic": "launj", "indonesia": "Ruang santai"},
        {"english": "Conference room", "phonetic": "kon-frens rum", "indonesia": "Ruang konferensi"},
        {"english": "Banquet hall", "phonetic": "ban-kwet hol", "indonesia": "Aula resepsi"},
        {"english": "Parking lot", "phonetic": "par-king lot", "indonesia": "Tempat parkir"},
        {"english": "Wi-Fi access", "phonetic": "wai fai ak-ses", "indonesia": "Akses Wi-Fi"},
        {"english": "Elevator", "phonetic": "e-le-ve-tor", "indonesia": "Lift"},
        {"english": "Room service", "phonetic": "rum ser-vis", "indonesia": "Layanan kamar"},
        {"english": "Laundry service", "phonetic": "lon-dri ser-vis", "indonesia": "Layanan binatu"},
        {"english": "Reception desk", "phonetic": "ri-sep-syen desk", "indonesia": "Meja resepsionis"},
        {"english": "Gift shop", "phonetic": "gift shop", "indonesia": "Toko oleh-oleh"},
        {"english": "Business center", "phonetic": "biz-nes sen-ter", "indonesia": "Pusat bisnis"},
        {"english": "Playground", "phonetic": "plei graund", "indonesia": "Taman bermain"},
        {"english": "Garden", "phonetic": "gar-den", "indonesia": "Taman"},
        {"english": "Mini bar", "phonetic": "mi-ni bar", "indonesia": "Mini bar"}
    ],

"16 - Hospitality Expressions": [
        {"english": "Welcome", "phonetic": "wel-kam", "indonesia": "Selamat datang"},
        {"english": "May I help you?", "phonetic": "mei ai help yu", "indonesia": "Bolehkah saya membantu Anda?"},
        {"english": "How can I assist you?", "phonetic": "hau ken ai e-sist yu", "indonesia": "Bagaimana saya bisa membantu Anda?"},
        {"english": "Please have a seat", "phonetic": "plis hev a sit", "indonesia": "Silakan duduk"},
        {"english": "Make yourself comfortable", "phonetic": "meik yor-self kom-fer-te-bel", "indonesia": "Buat diri Anda nyaman"},
        {"english": "Enjoy your stay", "phonetic": "en-joy yor stei", "indonesia": "Nikmati masa tinggal Anda"},
        {"english": "Have a nice day", "phonetic": "hev a nais dei", "indonesia": "Semoga harimu menyenangkan"},
        {"english": "Good morning", "phonetic": "gud mor-ning", "indonesia": "Selamat pagi"},
        {"english": "Good afternoon", "phonetic": "gud af-ter-nun", "indonesia": "Selamat siang"},
        {"english": "Good evening", "phonetic": "gud iv-ning", "indonesia": "Selamat malam"},
        {"english": "Good night", "phonetic": "gud nait", "indonesia": "Selamat tidur / malam"},
        {"english": "See you soon", "phonetic": "si yu sun", "indonesia": "Sampai jumpa"},
        {"english": "Thank you for coming", "phonetic": "thenk yu for ka-ming", "indonesia": "Terima kasih telah datang"},
        {"english": "We appreciate it", "phonetic": "wi a-pri-sie-it it", "indonesia": "Kami menghargainya"},
        {"english": "You’re welcome", "phonetic": "yor wel-kam", "indonesia": "Sama-sama"},
        {"english": "It’s our pleasure", "phonetic": "its aor ple-zher", "indonesia": "Dengan senang hati"},
        {"english": "Feel free", "phonetic": "fil fri", "indonesia": "Jangan sungkan"},
        {"english": "Excuse me", "phonetic": "eks-kyuz mi", "indonesia": "Permisi"},
        {"english": "Have a pleasant journey", "phonetic": "hev a ple-zent jer-ni", "indonesia": "Selamat jalan"},
        {"english": "Take care", "phonetic": "teik ker", "indonesia": "Hati-hati / jaga diri"}
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
    en_word = vocab["english"]
    ph_word = vocab["phonetic"]
    id_word = vocab["indonesia"]

    st.markdown(f"### {en_word} ({ph_word}) — *{id_word}*")

    components.html(
        f"""
        <div style="margin-bottom:15px;">
            <!-- Tombol TTS -->
            <button onclick="speakWord('{en_word}')">🔊 Pronounce</button>
            
            <!-- Tombol STT -->
            <button onclick="startRecognition('{en_word}')">🎙️ Test Speaking</button>
            <span id="result_{en_word.replace(" ", "_")}" style="margin-left:10px; font-weight:bold; color:gray;"></span>
        </div>

        <script>
        // TTS
        function speakWord(word) {{
            var utterance = new SpeechSynthesisUtterance(word);
            utterance.lang = "en-US";
            speechSynthesis.speak(utterance);
        }}

        function normalize(text) {{
            return text.toLowerCase()
                       .replace(/[^a-zA-Z\s]/g, "")
                       .trim();
        }}

        // STT
        function startRecognition(targetWord) {{
            var numberMap = {{
                "1": "one", "2": "two", "3": "three", "4": "four", "5": "five",
                "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten",
                "11": "eleven", "12": "twelve", "13": "thirteen", "14": "fourteen",
                "15": "fifteen", "16": "sixteen", "17": "seventeen", "18": "eighteen",
                "19": "nineteen", "20": "twenty"
            }};
            var ordinalMap = {{
                "1st": "first",
                "2nd": "second",
                "3rd": "third",
                "4th": "fourth",
                "5th": "fifth",
                "6th": "sixth",
                "7th": "seventh",
                "8th": "eighth",
                "9th": "ninth",
                "10th": "tenth",
                "11th": "eleventh",
                "12th": "twelfth",
                "13th": "thirteenth",
                "14th": "fourteenth",
                "15th": "fifteenth",
                "16th": "sixteenth",
                "17th": "seventeenth",
                "18th": "eighteenth",
                "19th": "nineteenth",
                "20th": "twentieth"
            }};
            var timeMap = {{
                "1 o'clock": ["1 o'clock", "one o'clock", "1", "one"],
                "2.15": ["2.15", "two fifteen", "quarter past two", "a quarter past two", "2:15"],
                "2.30": ["2.30", "two thirty", "half past two", "a half past two", "2:30"],
                "2.45": ["2.45", "two forty five", "quarter to three", "a quarter to three", "2:45"]
            }};
        
            var recognition = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = "en-US";
            recognition.start();
        
            recognition.onresult = function(event) {{
                var transcript = event.results[0][0].transcript.toLowerCase();
                var resultElem = document.getElementById("result_" + targetWord.replace(/ /g,"_"));
        
                function normalize(text) {{
                    return text.toLowerCase()
                               .replace(/[^a-zA-Z0-9\s]/g, "")
                               .trim();
                }}
        
                var normalizedTranscript = normalize(transcript);
                var normalizedTarget = normalize(targetWord);
        
                // Cek jika target adalah angka, bandingkan dengan kata
                if (numberMap[normalizedTarget] && normalizedTranscript === numberMap[normalizedTarget]) {{
                    resultElem.innerHTML = "✅ Benar (" + transcript + ")";
                    resultElem.style.color = "green";
                }}
                // Cek jika target adalah kata, bandingkan dengan angka juga
                else if (Object.keys(numberMap).find(key => numberMap[key] === normalizedTarget) === normalizedTranscript) {{
                    resultElem.innerHTML = "✅ Benar (" + transcript + ")";
                    resultElem.style.color = "green";
                }}
                // Cek normal (sama persis)
                else if (normalizedTranscript === normalizedTarget) {{
                    resultElem.innerHTML = "✅ Benar (" + transcript + ")";
                    resultElem.style.color = "green";
                }}
                else if (ordinalMap[normalizedTarget] && normalizedTranscript === ordinalMap[normalizedTarget]) {{
                    resultElem.innerHTML = "✅ Benar (" + transcript + ")";
                    resultElem.style.color = "green";
                }}
                // Cek jika target adalah kata ordinal, bandingkan dengan angka
                else if (Object.keys(ordinalMap).find(key => ordinalMap[key] === normalizedTarget) === normalizedTranscript) {{
                    resultElem.innerHTML = "✅ Benar (" + transcript + ")";
                    resultElem.style.color = "green";
                }}
                else if (timeMap[normalizedTarget]) {{
                    var validWords = timeMap[normalizedTarget].map(normalize);
                    if (validWords.includes(normalizedTranscript)) {{
                        resultElem.innerHTML = "✅ Benar (" + transcript + ")";
                        resultElem.style.color = "green";
                    }} else {{
                        resultElem.innerHTML = "❌ Salah (" + transcript + ")";
                        resultElem.style.color = "red";
                    }}
                }}
                else {{
                    resultElem.innerHTML = "❌ Salah (" + transcript + ")";
                    resultElem.style.color = "red";
                }}
            }};
        }}
        </script>
        """,
        height=80,
    )
