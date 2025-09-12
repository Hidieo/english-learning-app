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
        {"english": "Gym / fitness centre", "phonetic": "Jim", "indonesia": "Pusat kebugaran"},
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
        {"english": "Theme park / Amusement park", "phonetic": "tim park / e-myus-ment park", "indonesia": "Taman hiburan"},
        {"english": "Historical site", "phonetic": "his-to-ri-kel sait", "indonesia": "Situs bersejarah"},
        {"english": "Monument", "phonetic": "mo-nyu-ment", "indonesia": "Monumen"},
        {"english": "Church / Cathedral", "phonetic": "cerch / ka-tid-ral", "indonesia": "Gereja / Katedral"},
        {"english": "Mosque", "phonetic": "Mosk", "indonesia": "Masjid"},
        {"english": "Temple", "phonetic": "tem-pel", "indonesia": "Kuil / Pura"},
        {"english": "Cinema / Movie theater", "phonetic": "si-ne-ma / mu-vi thi-e-ter", "indonesia": "Bioskop"},
        {"english": "Stadium", "phonetic": "ste-di-em", "indonesia": "Stadion"},
        {"english": "Harbor / Port", "phonetic": "har-bor / port", "indonesia": "Pelabuhan"},
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
        {"english": "Go ahead / Go straight", "phonetic": "go e-hed / go streit", "indonesia": "Jalan lurus"},
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
        {"english": "Check-in", "phonetic": "cek-in", "indonesia": "Proses masuk hotel"},
        {"english": "Check out", "phonetic": "cek-aut", "indonesia": "Proses keluar hotel"},
        {"english": "Confirmation", "phonetic": "kon-fer-mey-syen", "indonesia": "Konfirmasi"},
        {"english": "Availability", "phonetic": "e-vei-le-bil-i-ti", "indonesia": "Ketersediaan"},
        {"english": "Single room", "phonetic": "sing-gal rum", "indonesia": "Kamar untuk satu orang"},
        {"english": "Double room", "phonetic": "dab-el rum", "indonesia": "Kamar untuk dua orang (1 ranjang)"},
        {"english": "Twin room", "phonetic": "twin rum", "indonesia": "Kamar dengan 2 ranjang terpisah"},
        {"english": "Suite", "phonetic": "suit (dibaca: swit)", "indonesia": "Kamar mewah / lebih besar"},
        {"english": "Deposit", "phonetic": "di-po-zit", "indonesia": "Uang muka / jaminan"},
        {"english": "Cancellation", "phonetic": "kan-se-lei-syen", "indonesia": "Pembatalan"},
        {"english": "Non-refundable", "phonetic": "non-ri-fan-de-bal", "indonesia": "Tidak bisa dikembalikan (uang)"},
        {"english": "Payment method", "phonetic": "pei-ment met-had", "indonesia": "Metode pembayaran"},
        {"english": "Credit card", "phonetic": "kred-it kard", "indonesia": "Kartu kredit"},
        {"english": "Guest", "phonetic": "gest", "indonesia": "Tamu"},
        {"english": "Reception", "phonetic": "ri-sep-syen", "indonesia": "Resepsionis / meja depan"},
        {"english": "Reservation number", "phonetic": "rez-er-vey-syen nam-ber", "indonesia": "Nomor pemesanan"},
        {"english": "Early check-in", "phonetic": "er-li cek-in", "indonesia": "Masuk lebih awal"},
        {"english": "Late check-out", "phonetic": "leit cek-aut", "indonesia": "Keluar lebih lambat"},
    ],
    "6 - Hotel Payments & Policies": [
        {"english": "Bill / Invoice", "phonetic": "Bil / in-vois", "indonesia": "Tagihan"},
        {"english": "Receipt", "phonetic": "Ri-sit", "indonesia": "Tanda terima"},
        {"english": "Payment method", "phonetic": "Pei-men met-hod", "indonesia": "Metode pembayaran"},
        {"english": "Cash", "phonetic": "Kesh", "indonesia": "Uang tunai"},
        {"english": "Check card", "phonetic": "Chek-kard", "indonesia": "Kartu debit"},
        {"english": "Feedback Form", "phonetic": "Fid-bek form", "indonesia": "Formulir masukan"},
        {"english": "Thank you for staying", "phonetic": "Thenk-yu for stei-ing", "indonesia": "Terima kasih telah menginap"},
        {"english": "Check-in time", "phonetic": "Cek-in taim", "indonesia": "Waktu check-in"},
        {"english": "Check-out time", "phonetic": "Cek-aut taim", "indonesia": "Waktu check-out"},
        {"english": "Early check-in", "phonetic": "Er-li cek-in", "indonesia": "Check-in lebih awal"},
        {"english": "Late check-out", "phonetic": "Leit cek-aut", "indonesia": "Check-out lebih lambat"},
        {"english": "Luggage / Baggage", "phonetic": "Lag-gej / Beg-ej", "indonesia": "Bagasi"},
        {"english": "Bellboy", "phonetic": "Bel-boi", "indonesia": "Petugas pengantar barang"},
        {"english": "Concierge", "phonetic": "Kon-si-erj", "indonesia": "Petugas layanan tamu"},
        {"english": "Front desk / Reception", "phonetic": "Fran-desk / Ri-sep-syen", "indonesia": "Resepsionis"},
        {"english": "Booking reference number", "phonetic": "Buk-ing re-fe-ren-si nam-ber", "indonesia": "Nomor referensi pemesanan"},
        {"english": "Room rate", "phonetic": "Rum reit", "indonesia": "Tarif kamar"},
        {"english": "Extension night", "phonetic": "Eks-ten-syen nait", "indonesia": "Perpanjangan malam menginap"},
        {"english": "Cancellation policy", "phonetic": "Kan-se-lei-syen po-li-si", "indonesia": "Kebijakan pembatalan"},
        {"english": "No-show", "phonetic": "Nou-syau", "indonesia": "Tamu tidak hadir"},
        {"english": "Upgrade room", "phonetic": "Ap-greid rum", "indonesia": "Peningkatan tipe kamar"},
    ],
    "7a - Hotel Facilities & Services": [
        {"english": "Gym", "phonetic": "jim", "indonesia": "Pusat kebugaran"},
        {"english": "Spa", "phonetic": "spa", "indonesia": "Spa / Tempat relaksasi"},
        {"english": "Business center", "phonetic": "biz-nes sen-ter", "indonesia": "Pusat bisnis"},
        {"english": "Shuttle service", "phonetic": "syatel ser-vis", "indonesia": "Layanan antar-jemput"},
        {"english": "24-hour reception", "phonetic": "twenti for awr ri-sep-syen", "indonesia": "Resepsionis 24 jam"},
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
        {"english": "Elevator / Lift", "phonetic": "e-le-ve-tor / lif", "indonesia": "Lift"},
        {"english": "Banquet hall", "phonetic": "ban-kuet hol", "indonesia": "Aula / Gedung perjamuan"},
        {"english": "Lobby", "phonetic": "lo-bi", "indonesia": "Lobi"},
        {"english": "Front desk", "phonetic": "frant desk", "indonesia": "Meja resepsionis"},
        {"english": "Gift shop", "phonetic": "gift shop", "indonesia": "Toko cenderamata"},
        {"english": "Laundry service", "phonetic": "lon-dri ser-vis", "indonesia": "Layanan binatu/cuci"},
        {"english": "Valet parking", "phonetic": "va-lei par-king", "indonesia": "Parkir valet"},
        {"english": "ATM / Cash machine", "phonetic": "ei-ti-em / kesh me-shin", "indonesia": "Mesin ATM"},
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
        {"english": "Well-equipped", "phonetic": "Wel-i-kwip", "indonesia": "Dilengkapi dengan baik"},
        {"english": "Convenient", "phonetic": "Kon-vini-en", "indonesia": "Praktis/mudah diakses"},
        {"english": "Private", "phonetic": "Prai-vet", "indonesia": "Pribadi"},
        {"english": "Quiet", "phonetic": "Kwai-et", "indonesia": "Tenang"},
        {"english": "Bright", "phonetic": "brait", "indonesia": "Terang"},
        {"english": "Affordable", "phonetic": "Afor-dabel", "indonesia": "Terjangkau"},
        {"english": "Impressive", "phonetic": "im-presif", "indonesia": "Mengesankan"},
        {"english": "Relaxing", "phonetic": "ri-lek-sing", "indonesia": "Menyenangkan"},
        {"english": "Family-friendly", "phonetic": "Fae-mili fren-li", "indonesia": "Ramah untuk keluarga"},
        {"english": "Scenic", "phonetic": "sinik", "indonesia": "Indah (pemandangan)"},
        {"english": "Accessible", "phonetic": "Akses-sebel", "indonesia": "Mudah diakses"},
    ]
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
