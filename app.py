import streamlit as st
import pandas as pd
import time

# Configure page settings
st.set_page_config(
    page_title="PLC Obat - Media Pembelajaran Farmasi",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #f8fafc;
    }
    
    /* Header banner styling */
    .hero-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    .hero-banner h1 {
        color: #ffffff !important;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .hero-banner p {
        color: #e0f2fe;
        font-size: 1.1rem;
    }
    
    /* Custom Card Styling */
    .stage-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 6px solid #3b82f6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.25rem;
        transition: transform 0.2s ease;
    }
    .stage-card:hover {
        transform: translateY(-2px);
    }
    .analogy-box {
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #166534;
        font-size: 0.95rem;
        margin-top: 0.5rem;
    }
    
    /* Question card styling */
    .quiz-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    /* Score card badge */
    .badge-success {
        background-color: #dcfce7;
        color: #15803d;
        padding: 0.5rem 1rem;
        border-radius: 9999px;
        font-weight: bold;
    }
    
    /* Custom divider */
    hr {
        border-top: 2px solid #e2e8f0;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)


if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_class' not in st.session_state:
    st.session_state.user_class = "Fase E - Farmasi"
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}


QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "1. Tahapan awal di mana ilmuwan mencari dan menguji molekul/senyawa kimia baru untuk mengobati penyakit disebut...",
        "options": ["Registrasi Obat", "Formulasi Sediaan", "Riset & Pengembangan (R&D)", "Product Recall"],
        "answer": "Riset & Pengembangan (R&D)",
        "explanation": "Tahap R&D adalah langkah pertama untuk menemukan kandidat obat baru melalui identifikasi senyawa dan uji praklinis."
    },
    {
        "id": 2,
        "question": "2. Menentukan apakah obat akan dibuat dalam bentuk tablet, kapsul, sirup, atau injeksi merupakan fokus utama pada tahap...",
        "options": ["Distribusi", "Formulasi", "Penjualan Pasar", "Pemusnahan Limbah"],
        "answer": "Formulasi",
        "explanation": "Formulasi merancang sediaan fisik obat beserta eksipien (zat tambahan) agar obat efektif, stabil, dan nyaman dikonsumsi."
    },
    {
        "id": 3,
        "question": "3. Lembaga resmi di Indonesia yang berwenang mengevaluasi dokumen teknis dan memberikan Izin Edar (NIE) obat adalah...",
        "options": ["Kementerian Kesehatan (Kemenkes)", "Ikatan Dokter Indonesia (IDI)", "Badan Pengawas Obat dan Makanan (BPOM)", "PT Kimia Farma"],
        "answer": "Badan Pengawas Obat dan Makanan (BPOM)",
        "explanation": "BPOM bertugas mengawasi dan memberikan Nomor Izin Edar (NIE) sebelum obat legal dipasarkan di Indonesia."
    },
    {
        "id": 4,
        "question": "4. Apa tujuan utama dari pelaksanaan Uji Praklinis pada tahap Riset & Pengembangan?",
        "options": [
            "Menentukan harga jual produk di apotek",
            "Melihat profil keamanan dan efektivitas awal pada tingkat sel atau hewan coba",
            "Mencetak kemasan dan merancang iklan",
            "Melakukan promosi langsung kepada dokter dan rumah sakit"
        ],
        "answer": "Melihat profil keamanan dan efektivitas awal pada tingkat sel atau hewan coba",
        "explanation": "Uji praklinis dilakukan pada sel (in vitro) atau hewan (in vivo) sebelum uji klinis dilakukan pada manusia."
    },
    {
        "id": 5,
        "question": "5. Jika industri farmasi menemukan satu batch obat mengalami keretakan tablet atau kontaminasi saat sudah di pasaran, langkah wajibnya adalah...",
        "options": [
            "Membiarkannya hingga masa kadaluarsa habis",
            "Memberikan diskon besar-besaran",
            "Melakukan Product Recall (Penarikan Produk)",
            "Mengganti nama merek obat tersebut"
        ],
        "answer": "Melakukan Product Recall (Penarikan Produk)",
        "explanation": "Product Recall wajib dilakukan untuk melindungi keselamatan masyarakat dari cacat mutu atau bahaya obat."
    },
    {
        "id": 6,
        "question": "6. Urutan yang benar dalam siklus hidup produk obat (Product Life Cycle) secara umum adalah...",
        "options": [
            "Registrasi → Formulasi → R&D → Product Recall",
            "R&D → Formulasi → Registrasi → Produksi & Pemasaran → Post-Marketing / Recall",
            "Formulasi → R&D → Product Recall → Registrasi",
            "Registrasi → R&D → Formulasi → Produksi & Pemasaran"
        ],
        "answer": "R&D → Formulasi → Registrasi → Produksi & Pemasaran → Post-Marketing / Recall",
        "explanation": "Siklus obat diawali dari R&D, penentuan Formulasi, Registrasi Izin Edar, Produksi Massal & Pemasaran, hingga Pemantauan Pasar."
    },
    {
        "id": 7,
        "question": "7. Kegiatan memastikan agar zat aktif tidak terurai dan tetap stabil selama masa simpan (shelf-life) terjadi pada tahap...",
        "options": ["Registrasi", "Pemasaran Iklan", "Formulasi & Uji Stabilitas", "Pengemasan Sekunder"],
        "answer": "Formulasi & Uji Stabilitas",
        "explanation": "Uji stabilitas dilakukan saat formulasi untuk menentukan umur simpan obat dan kondisi penyimpanan yang tepat."
    },
    {
        "id": 8,
        "question": "8. Manakah di bawah ini yang BUKAN merupakan alasan dilakukannya Product Recall?",
        "options": [
            "Ditemukannya kontaminasi zat berbahaya pada obat",
            "Obat mengalami reaksi efek samping berat yang tak terduga",
            "Penjualan produk sangat laris dan diminati masyarakat",
            "Dosis zat aktif tidak sesuai dengan spesifikasi yang disetujui BPOM"
        ],
        "answer": "Penjualan produk sangat laris dan diminati masyarakat",
        "explanation": "Penjualan yang laris adalah indikator keberhasilan pasar, bukan alasan penarikan produk (recall)."
    },
    {
        "id": 9,
        "question": "9. Dokumen Dossier yang berisi data uji klinis, hasil uji stabilitas, dan proses pembuatan obat diserahkan pada tahap...",
        "options": ["Riset Pasar", "Registrasi Obat", "Penarikan Obat", "Pengolahan Limbah"],
        "answer": "Registrasi Obat",
        "explanation": "Dokumen registrasi lengkap diserahkan kepada badan regulator (BPOM) untuk membuktikan safety, efficacy, and quality."
    },
    {
        "id": 10,
        "question": "10. Mengapa pengawasan Siklus Hidup Produk Obat jauh lebih ketat dibandingkan dengan produk konsumen umum (seperti pakaian)?",
        "options": [
            "Karena biaya pembuatan obat sangat mahal",
            "Kerap berhubungan langsung dengan kesehatan, keselamatan, dan jiwa manusia",
            "Pabrik obat membutuhkan area tanah yang sangat luas",
            "Bahan baku obat hanya bisa diimpor dari luar negeri"
        ],
        "answer": "Kerap berhubungan langsung dengan kesehatan, keselamatan, dan jiwa manusia",
        "explanation": "Obat adalah produk khusus (high regulated) yang dampaknya langsung mempengaruhi organ tubuh dan jiwa pasien."
    }
]


with st.sidebar:
    st.image("https://img.icons8.com/illustrations/100/pill.png", width=80)
    st.title("💊 Media PLC Obat")
    st.caption("Fase E - Dasar-Dasar Keahlian Farmasi")
    
    st.divider()
    
    st.subheader("👤 Identitas Peserta Didik")
    st.session_state.user_name = st.text_input("Nama Lengkap", st.session_state.user_name, placeholder="Contoh: Budi Santoso")
    st.session_state.user_class = st.text_input("Kelas / Rombel", st.session_state.user_class)
    
    st.divider()
    
    menu = st.radio(
        "📌 Navigasi Pembelajaran:",
        [
            "1. Materi & Visualisasi PLC",
            "2. Interactive Flowchart Journey",
            "3. Kuis Interaktif (10 Soal)",
            "4. Rubrik Refleksi Diri"
        ]
    )
    
    st.divider()
    st.info("💡 **Petunjuk:** Pelajari materi visual terlebih dahulu sebelum mengerjakan Kuis dan Rubrik Refleksi!")


st.markdown("""
<div class="hero-banner">
    <h1>Perjalanan Sebuah Obat (Product Life Cycle)</h1>
    <p>Media Pembelajaran Interaktif untuk Peserta Didik Fase E SMK Farmasi</p>
</div>
""", unsafe_allow_html=True)


if menu == "1. Materi & Visualisasi PLC":
    st.header("📘 Materi Pembelajaran: The Journey of a Pill")
    st.write("""
    Bayangkan sebuah obat adalah seorang **pahlawan** yang harus melewati berbagai ujian dan sertifikasi ketat 
    sebelum akhirnya diizinkan untuk menolong dan menyembuhkan masyarakat!
    """)
    
    # Overview Progress Steps
    st.subheader("🔄 5 Tahapan Utama Siklus Hidup Produk Obat")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Tahap 1", "🔬 R&D", "Riset")
    with col2:
        st.metric("Tahap 2", "🧪 Formulasi", "Sediaan")
    with col3:
        st.metric("Tahap 3", "📜 Registrasi", "Izin BPOM")
    with col4:
        st.metric("Tahap 4", "🏭 Produksi", "Pemasaran")
    with col5:
        st.metric("Tahap 5", "🛡️ Surveillance", "Recall")
        
    st.divider()
    
    # Detailed Cards for Each Stage
    st.subheader("📖 Penjelasan Rinci Setiap Tahapan")
    
    # Stage 1
    st.markdown("""
    <div class="stage-card" style="border-left-color: #3b82f6;">
        <h3>1. Tahap Riset & Pengembangan (Research & Development - R&D)</h3>
        <p><b>Aktivitas Utama:</b> Penemuan molekul/senyawa baru, sintesis bahan aktif, dan uji praklinis pada kultur sel serta hewan coba untuk melihat efektivitas awal dan tingkat racun (toksisitas).</p>
        <div class="analogy-box">
            <b>💡 Analogi:</b> Seperti tim ilmuwan yang mencari bahan racikan rahasia terkuat untuk ramuan pahlawan super.
        </div>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("🔍 Detail Teknis Tahap R&D"):
        st.write("""
        - **Target Identification:** Menentukan molekul spesifik di dalam tubuh yang akan diintervensi oleh obat.
        - **Uji Praklinis:** Menguji keamanan pada hewan coba (seperti mencit atau kelinci) sebelum diuji ke manusia.
        """)

    # Stage 2
    st.markdown("""
    <div class="stage-card" style="border-left-color: #8b5cf6;">
        <h3>2. Tahap Formulasi (Formulation Development)</h3>
        <p><b>Aktivitas Utama:</b> Menentukan bentuk sediaan obat yang paling cocok (tablet, sirup, kapsul, atau injeksi), memilih eksipien (zat tambahan), serta menguji stabilitas fisika-kimia obat.</p>
        <div class="analogy-box">
            <b>💡 Analogi:</b> Memasak ramuan tersebut menjadi makanan yang rasanya enak, tahan lama, dan mudah dikonsumsi.
        </div>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("🔍 Detail Teknis Tahap Formulasi"):
        st.write("""
        - **Studi Preformulasi:** Mempelajari sifat fisika dan kimia bahan aktif obat.
        - **Uji Stabilitas Accelerate:** Menyimpan obat pada suhu & kelembapan tinggi untuk memprediksi tanggal kadaluarsa (*shelf-life*).
        """)

    # Stage 3
    st.markdown("""
    <div class="stage-card" style="border-left-color: #eab308;">
        <h3>3. Tahap Registrasi & Evaluasi BPOM</h3>
        <p><b>Aktivitas Utama:</b> Mengajukan pendaftaran dokumen teknis (Dossier) obat ke BPOM untuk mendapatkan Nomor Izin Edar (NIE) agar legal dipasarkan.</p>
        <div class="analogy-box">
            <b>💡 Analogi:</b> Mengajukan paspor dan visa resmi agar sang pahlawan boleh bepergian dan bertugas di tengah masyarakat.
        </div>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("🔍 Detail Teknis Tahap Registrasi"):
        st.write("""
        - **Efficacy & Safety Evaluation:** Tim pakar BPOM menilai apakah manfaat obat jauh lebih besar daripada risiko efek sampingnya.
        - **NIE (Nomor Izin Edar):** Kode unik 15 digit yang wajib dicantumkan pada kemasan obat.
        """)

    # Stage 4
    st.markdown("""
    <div class="stage-card" style="border-left-color: #10b981;">
        <h3>4. Tahap Produksi Massal & Pemasaran</h3>
        <p><b>Aktivitas Utama:</b> Pembuatan obat skala besar di industri farmasi menggunakan standar CPOB (Cara Pembuatan Obat yang Baik) serta distribusi ke apotek, klinik, dan rumah sakit.</p>
        <div class="analogy-box">
            <b>💡 Analogi:</b> Pahlawan dikloning secara presisi di pabrik canggih dan dikirim ke seluruh penjuru kota.
        </div>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("🔍 Detail Teknis Tahap Produksi & Pemasaran"):
        st.write("""
        - **CPOB / GMP:** Menjamin obat dibuat secara konsisten sesuai standar mutu.
        - **Marketing & Edukasi:** Memberikan informasi yang jujur kepada tenaga medis (dokter/apoteker) mengenai dosis dan indikasi obat.
        """)

    # Stage 5
    st.markdown("""
    <div class="stage-card" style="border-left-color: #ef4444;">
        <h3>5. Post-Marketing Surveillance & Product Recall</h3>
        <p><b>Aktivitas Utama:</b> Memantau efek samping obat yang baru muncul di masyarakat (Farmakovigilans). Jika ditemukan cacat kualitas atau bahaya fatal, obat ditarik dari peredaran.</p>
        <div class="analogy-box">
            <b>💡 Analogi:</b> Tim penyelamat segera menarik kembali pahlawan jika ditemukan cacat agar tidak membahayakan warga.
        </div>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("🔍 Detail Teknis Product Recall"):
        st.write("""
        - **CPOB Class 1 Recall:** Penarikan obat yang dapat menyebabkan efek kesehatan serius atau kematian.
        - **CPOB Class 2/3 Recall:** Penarikan karena masalah kelengkapan etiket atau cacat fisik ringan.
        """)


elif menu == "2. Interactive Flowchart Journey":
    st.header("🎮 Simulator Perjalanan Obat")
    st.write("Klik setiap tahapan di bawah untuk mensimulasikan keputusan yang diambil dalam industri farmasi!")

    selected_stage = st.select_slider(
        "Pilih Tahapan Produk Obat:",
        options=["1. R&D", "2. Formulasi", "3. Registrasi BPOM", "4. Produksi & Pasar", "5. Post-Market Monitoring"]
    )
    
    st.divider()
    
    if selected_stage == "1. R&D":
        st.subheader("🔬 Tahap 1: Penemuan & Uji Praklinis")
        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.write("""
            Para peneliti berhasil mensintesis molekul senyawa **X-123** untuk mengobati demam tinggi.
            Sebelum dicoba ke manusia, senyawa ini diuji pada sel dan hewan coba.
            """)
            status = st.radio("Hasil Uji Praklinis Toksisitas:", ["Lolos (Sangat Aman pada Hewan)", "Gagal (Beracun pada Sel Hati)"])
            if status == "Lolos (Sangat Aman pada Hewan)":
                st.success("✅ **Lanjut ke Tahap Formulasi!** Molekul aman dan efektif.")
            else:
                st.error("❌ **Proyek Dihentikan!** Molekul terlalu beracun. Tim R&D harus mencari molekul lain.")
        with col_b:
            st.info("📊 **Status R&D:**\n- Estimasi Waktu: 2-5 Tahun\n- Biaya: Tinggi\n- Risiko Gagal: Sangat Tinggi")

    elif selected_stage == "2. Formulasi":
        st.subheader("🧪 Tahap 2: Pengembangan Sediaan Obat")
        st.write("Molekul **X-123** akan dibuat menjadi bentuk obat padat atau cair.")
        sediaan = st.selectbox("Pilih Bentuk Sediaan:", ["Tablet Salut Selaput (Paling Stabil)", "Sirup (Anak-anak)", "Injeksi (Gawat Darurat)"])
        
        st.write(f"Anda memilih sediaan: **{sediaan}**")
        st.info("⚙️ Tim Formulasi sedang melakukan *Uji Stabilitas Dipercepat* pada suhu 40°C dan RH 75%.")
        st.progress(100)
        st.success("✅ Formulasi terbukti stabil selama 2 tahun masa simpan!")

    elif selected_stage == "3. Registrasi BPOM":
        st.subheader("📜 Tahap 3: Pengajuan Izin Edar BPOM")
        st.write("Seluruh dokumen uji klinis, formulasi, dan mutu diserahkan ke evaluator BPOM.")
        
        kelengkapan = st.checkbox("Dokumen Uji Stabilitas Lengkap")
        kelengkapan_2 = st.checkbox("Sertifikat CPOB Pabrik Aktif")
        
        if kelengkapan and kelengkapan_2:
            st.balloons()
            st.success("🎉 **SELAMAT! BPOM menerbitkan Nomor Izin Edar (NIE): DKL2412345610A1**")
        else:
            st.warning("⚠️ Dokumen belum lengkap. BPOM mengeluarkan Surat Permintaan Tambahan Data.")

    elif selected_stage == "4. Produksi & Pasar":
        st.subheader("🏭 Tahap 4: Komersialisasi & Pembuatan Massal")
        st.write("Pabrik memproduksi 1.000.000 strip tablet obat X-123.")
        st.image("https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800", caption="Produksi Obat Massal Berdasarkan Standar CPOB", use_container_width=True)
        st.success("📦 Obat berhasil didistribusikan ke Pedagang Besar Farmasi (PBF), Rumah Sakit, dan Apotek.")

    elif selected_stage == "5. Post-Market Monitoring":
        st.subheader("🛡️ Tahap 5: Pemantauan Efek Samping & Recall")
        st.write("Setelah 6 bulan dipasarkan, terdapat laporan dari Apotek bahwa terjadi perubahan warna pada Batch Nomor **B24001**.")
        
        tindakan = st.radio("Tindakan Industri Farmasi:", [
            "Lakukan Product Recall (Penarikan Obat) Khusus Batch B24001",
            "Abaikan Laporan dan Tetap Menjual Obat",
            "Ganti Kemasan Obat Tanpa Menarik Produk"
        ])
        
        if tindakan == "Lakukan Product Recall (Penarikan Obat) Khusus Batch B24001":
            st.success("🎯 **Keputusan Tepat!** Industri farmasi bertanggung jawab menarik obat demi keselamatan konsumen sesuai standar CPOB.")
        else:
            st.error("🚨 **KEPUTUSAN BAHAYA!** Menjual obat rusak melanggar hukum dan membahayakan keselamatan pasien.")


elif menu == "3. Kuis Interaktif (10 Soal)":
    st.header("📝 Kuis Pilihan Ganda (10 Soal)")
    st.write("Uji pemahaman Anda mengenai siklus hidup produk obat. Pilihlah jawaban yang paling tepat!")
    
    if not st.session_state.user_name:
        st.warning("⚠️ Silakan isi Nama Lengkap Anda di sidebar kiri terlebih dahulu sebelum memulai kuis!")
    
    with st.form("quiz_form"):
        temp_answers = {}
        for q in QUIZ_QUESTIONS:
            st.markdown(f"**{q['question']}**")
            selected_option = st.radio(
                "Pilih jawaban:",
                options=q["options"],
                key=f"q_{q['id']}",
                index=None
            )
            temp_answers[q['id']] = selected_option
            st.markdown("<br>", unsafe_allow_html=True)
            
        submitted = st.form_submit_button("🚀 Kirim & Periksa Jawaban", type="primary")
        
        if submitted:
            st.session_state.user_answers = temp_answers
            st.session_state.quiz_submitted = True
            
            # Calculate Score
            score = 0
            for q in QUIZ_QUESTIONS:
                if temp_answers.get(q['id']) == q['answer']:
                    score += 10
            st.session_state.quiz_score = score

    # Display Quiz Results
    if st.session_state.quiz_submitted:
        st.divider()
        st.subheader("📊 Hasil Kuis Anda")
        
        col_res1, col_res2 = st.columns([1, 2])
        with col_res1:
            score = st.session_state.quiz_score
            st.metric("Skor Akhir", f"{score} / 100")
            if score >= 80:
                st.success("🌟 Predikat: **Sangat Baik (Apoteker Muda Pro)**")
            elif score >= 60:
                st.info("👍 Predikat: **Baik (Cukup Paham)**")
            else:
                st.error("📖 Predikat: **Perlu Belajar Lagi**")
                
        with col_res2:
            st.write(f"**Nama:** {st.session_state.user_name if st.session_state.user_name else 'Anonim'}")
            st.write(f"**Kelas:** {st.session_state.user_class}")
            st.write("Lihat pembahasan detail di bawah untuk setiap soal:")

        st.subheader("🔍 Pembahasan & Detail Jawaban")
        for q in QUIZ_QUESTIONS:
            user_ans = st.session_state.user_answers.get(q['id'])
            correct_ans = q['answer']
            
            with st.expander(f"Soal No. {q['id']} - {'✅ Benar' if user_ans == correct_ans else '❌ Salah'}"):
                st.write(f"**Jawaban Anda:** {user_ans if user_ans else 'Tidak dijawab'}")
                st.write(f"**Jawaban Benar:** {correct_ans}")
                st.info(f"💡 **Penjelasan:** {q['explanation']}")


elif menu == "4. Rubrik Refleksi Diri":
    st.header("🪞 Rubrik Asesmen Mandiri (Assessment as Learning)")
    st.write("""
    Gunakan tabel refleksi diri ini untuk menilai tingkat pemahaman Anda secara jujur. 
    Hasil ini membantu Anda menentukan langkah belajar selanjutnya!
    """)
    
    st.info(f"👤 **Nama Siswa:** {st.session_state.user_name if st.session_state.user_name else 'Belum Diisi'} | **Kelas:** {st.session_state.user_class}")
    
    rubric_questions = [
        "1. Saya mampu menjelaskan perbedaan utama antara tahap Riset & Pengembangan (R&D) dan Formulasi.",
        "2. Saya memahami pentingnya peran BPOM dalam menerbitkan Nomor Izin Edar (NIE) pada tahap Registrasi.",
        "3. Saya dapat memberikan contoh alasan mengapa sebuah obat harus ditarik dari peredaran (Product Recall).",
        "4. Saya dapat menyebutkan urutan logis siklus hidup produk obat dari R&D hingga Post-Marketing Surveillance.",
        "5. Saya menyadari tanggung jawab besar industri farmasi dalam menjamin keamanan obat bagi pasien."
    ]
    
    scale_options = {
        4: "Sangat Paham (4)",
        3: "Paham (3)",
        2: "Cukup Paham (2)",
        1: "Perlu Belajar Lagi (1)"
    }
    
    ref_scores = []
    
    st.subheader("📋 Lembar Refleksi Diri")
    for i, q in enumerate(rubric_questions, start=1):
        st.write(f"**{q}**")
        val = st.select_slider(
            f"Tingkat Pemahaman Poin {i}:",
            options=[1, 2, 3, 4],
            format_func=lambda x: scale_options[x],
            key=f"ref_{i}",
            value=3
        )
        ref_scores.append(val)
        st.markdown("---")
        
    avg_score = sum(ref_scores) / len(ref_scores)
    
    st.subheader("📊 Analisis Hasil Refleksi Diri")
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.metric("Rata-Rata Skala Pemahaman", f"{avg_score:.2f} / 4.0")
        st.progress(avg_score / 4.0)
        
    with col_b:
        if avg_score >= 3.5:
            st.success("🎉 **Luar Biasa!** Anda telah menguasai seluruh konsep Product Life Cycle obat dengan sangat baik.")
        elif avg_score >= 2.5:
            st.info("👍 **Bagus!** Anda sudah memahami sebagian besar konsep. Tinjau kembali beberapa poin materi yang masih ragu.")
        else:
            st.warning("💡 **Rencana Tindak Lanjut Recommended:** Pelajari kembali materi visual di menu 1, tanyakan poin yang belum paham kepada Guru, atau berdiskusi dengan teman sekelompok!")

    # Summary Table Display
    ref_df = pd.DataFrame({
        "Pernyataan Refleksi": [f"Poin {i}" for i in range(1, 6)],
        "Skor Self-Assessment": ref_scores,
        "Kategori": [scale_options[s] for s in ref_scores]
    })
    
    st.table(ref_df)


st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("✨ Media Pembelajaran Digital Farmasi - Capaian Pembelajaran Fase E (Kurikulum Merdeka)")
