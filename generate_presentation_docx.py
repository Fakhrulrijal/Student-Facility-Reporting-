import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_document():
    doc = Document()

    # Set Margins 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Colors
    PRIMARY = RGBColor(0x1E, 0x3A, 0x8A)     # Dark Blue
    SECONDARY = RGBColor(0x25, 0x63, 0xEB)   # Royal Blue
    TEXT_DARK = RGBColor(0x0F, 0x17, 0x2A)   # Slate 900
    MUTED = RGBColor(0x64, 0x74, 0x8B)       # Slate 500
    GREEN = RGBColor(0x15, 0x80, 0x3D)       # Green 700
    AMBER = RGBColor(0xB4, 0x53, 0x09)       # Amber 700

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("NASKAH PRESENTASI AKHIR PROYEK\nAPLIKASI PELAPORAN FASILITAS KAMPUS BERBASIS AI & MOBILE")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(20)
    run_title.font.bold = True
    run_title.font.color.rgb = PRIMARY

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("Panduan Komprehensif Presentasi & Demonstrasi Hasil 6 Modul Lengkap (MOD-01 s/d MOD-06)\nUntuk Evaluasi Dosen Pembimbing / Penguji (Pak Mansyur)")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = MUTED

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Info Box Table
    info_table = doc.add_table(rows=4, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Mata Kuliah / Tugas", "Pengembangan Aplikasi Mobile & AI (Tugas Modul Pak Mansyur)"),
        ("Judul Proyek", "Aplikasi Pelaporan Fasilitas Kampus Berbasis AI & Mobile"),
        ("Cakupan Modul", "6 Modul Lengkap (MOD-01, MOD-02, MOD-03, MOD-04, MOD-05, MOD-06)"),
        ("Teknologi Utama", "Flutter (Dart), Python FastAPI, Google Gemini AI SDK, JSON Database")
    ]
    for i, (k, v) in enumerate(info_data):
        row = info_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0)
        set_cell_margins(c1)
        r0 = c0.paragraphs[0].add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(10)
        r0.font.color.rgb = TEXT_DARK
        r1 = c1.paragraphs[0].add_run(v)
        r1.font.size = Pt(10)
        r1.font.color.rgb = TEXT_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    def add_section_heading(title, subtitle=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.font.name = "Calibri"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = PRIMARY
        if subtitle:
            p_sub = doc.add_paragraph()
            p_sub.paragraph_format.space_after = Pt(8)
            p_sub.paragraph_format.keep_with_next = True
            run_sub = p_sub.add_run(subtitle)
            run_sub.font.italic = True
            run_sub.font.size = Pt(10.5)
            run_sub.font.color.rgb = MUTED

    def add_speech_bubble(speaker, speech_text, action_cue=None):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        cell.width = Inches(6.5)
        set_cell_background(cell, "EFF6FF")
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(4)
        r_spk = p.add_run(f"🗣️ {speaker}:")
        r_spk.font.bold = True
        r_spk.font.size = Pt(11)
        r_spk.font.color.rgb = PRIMARY

        if action_cue:
            p_cue = cell.add_paragraph()
            p_cue.paragraph_format.space_after = Pt(6)
            r_cue = p_cue.add_run(f"🎬 [AKSI DEMO / SLIDE]: {action_cue}")
            r_cue.font.bold = True
            r_cue.font.size = Pt(10)
            r_cue.font.color.rgb = AMBER

        p_txt = cell.add_paragraph()
        p_txt.paragraph_format.space_after = Pt(0)
        r_txt = p_txt.add_run(f'"{speech_text}"')
        r_txt.font.size = Pt(11)
        r_txt.font.italic = True
        r_txt.font.color.rgb = TEXT_DARK

        doc.add_paragraph().paragraph_format.space_after = Pt(8)

    def add_bullet_point(label, desc):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        r_lbl = p.add_run(f"{label}: ")
        r_lbl.font.bold = True
        r_lbl.font.size = Pt(10.5)
        r_lbl.font.color.rgb = TEXT_DARK
        r_desc = p.add_run(desc)
        r_desc.font.size = Pt(10.5)
        r_desc.font.color.rgb = TEXT_DARK

    # =========================================================================
    # 1. BAGIAN PEMBUKA
    # =========================================================================
    add_section_heading("BAGIAN 1: PEMBUKAAN & LATAR BELAKANG PROYEK", "Estimasi Waktu: 2 Menit")
    add_speech_bubble(
        "Presenter / Pembicara",
        "Selamat pagi/siang kepada Bapak Mansyur dan rekan-rekan sekalian. Terima kasih atas kesempatan yang diberikan kepada kelompok kami. "
        "Pada hari ini, kami akan mempresentasikan sekaligus mendemonstrasikan hasil implementasi lengkap dari 6 modul sistem Aplikasi Pelaporan Fasilitas Kampus Berbasis AI dan Mobile.\n\n"
        "Latar belakang proyek ini berangkat dari permasalahan nyata di lingkungan kampus kita, di mana pelaporan kerusakan fasilitas sering kali dilakukan secara manual, "
        "laporan tercecer di grup chat, lambat ditindaklanjuti, dan petugas fasilitas kesulitan menentukan fasilitas mana yang harus diperbaiki terlebih dahulu. "
        "Oleh karena itu, kami membangun solusi terintegrasi berbasis Mobile dan AI yang menghubungkan mahasiswa, dosen, serta biro logistik/admin kampus secara transparan dan cerdas.",
        "Tampilkan slide judul presentasi atau layar awal aplikasi di laptop/layar proyektor."
    )
    p_tech = doc.add_paragraph()
    r = p_tech.add_run("Pilar Arsitektur & Teknologi yang Digunakan:")
    r.font.bold = True
    r.font.size = Pt(11)
    add_bullet_point("Frontend Mobile/Web", "Flutter 3 dengan arsitektur MultiProvider, Clean State Management, dan Material 3 Design.")
    add_bullet_point("Backend REST API", "Python FastAPI berkecepatan tinggi dengan auto-generated OpenAPI/Swagger documentation.")
    add_bullet_point("AI Engine", "Google Gemini API SDK (gemini-2.5-flash) yang didukung Smart Empirical Heuristic Fallback.")
    add_bullet_point("Database & Storage", "JSON File Database terstruktur (menyimpan relasi PENGGUNA, LAPORAN, FASILITAS, STATUS_TIKET, TINDAKAN_PENANGANAN, ANALISIS_AI) serta Firebase Storage & FCM Push Notifications.")

    # =========================================================================
    # 2. MODUL 1
    # =========================================================================
    add_section_heading("BAGIAN 2: MODUL 1 (MOD-01) — AUTENTIKASI & USER MANAGEMENT", "Estimasi Waktu: 2 Menit")
    add_speech_bubble(
        "Presenter / Pembicara",
        "Kita mulai dari gerbang pertama sistem, yaitu Modul 1: Autentikasi dan Manajemen Akun. "
        "Di modul ini, kami memastikan keamanan akses dan pemisahan hak akses antara Civitas Akademika (Mahasiswa/Dosen) dan Administrator Fasilitas.\n\n"
        "Fitur unggulan pada Modul 1 adalah validasi data berlapis: NIM atau NIP wajib numerik 8 digit, email wajib menggunakan domain resmi kampus yaitu @kampus.ac.id, "
        "dan kata sandi minimal 8 karakter. Seluruh kata sandi dienkripsi menggunakan algoritma Bcrypt Hashing satu arah, "
        "dan sesi login dilindungi oleh JWT (JSON Web Token) Bearer Token berstandar industri.",
        "Buka halaman Login di aplikasi. Tunjukkan tombol 'Simulasi Mahasiswa' dan 'Simulasi Admin', lalu tunjukkan respon login berhasil."
    )
    add_bullet_point("Hak Akses Mahasiswa", "Dapat membuat laporan kerusakan, memindai QR aset fasilitas, dan melacak histori status tiket miliknya.")
    add_bullet_point("Hak Akses Admin", "Dapat mengakses Dashboard Metrik, memverifikasi laporan (Terima/Tolak), menjadwalkan teknisi, mengakses Rangkuman AI, dan melihat Urutan Prioritas Scoring AI.")
    add_bullet_point("Hasil Uji Modul 1", "Lolos 100% pada pengujian otomatis test_all_modules.py (validasi NIM pendek, email non-kampus tertolak HTTP 422, dan login via Bcrypt hash sukses).")

    # =========================================================================
    # 3. MODUL 2
    # =========================================================================
    add_section_heading("BAGIAN 3: MODUL 2 (MOD-02) — PELAPORAN KERUSAKAN & QR SCANNER", "Estimasi Waktu: 2.5 Menit")
    add_speech_bubble(
        "Presenter / Pembicara",
        "Selanjutnya adalah Modul 2: Inti dari proses pelaporan fasilitas. Mahasiswa sering kali bingung menyebutkan nama ruangan atau kode inventaris secara presisi. "
        "Untuk mengatasi hal tersebut, kami mengintegrasikan pemindai QR Code Fasilitas.\n\n"
        "Ketika mahasiswa memindai stiker QR pada aset (misalnya kode 'KR-A002-07'), sistem backend secara otomatis melakukan lookup dan mengisi lokasi gedung (Ruang A002 Gedung A) "
        "serta kategori fasilitas (Kursi Kuliah) secara instan. Jika QR rusak, kami menyediakan fallback input lokasi manual.\n\n"
        "Mahasiswa kemudian mengambil bukti foto kerusakan, memilih tingkat keparahan (Ringan, Sedang, Berat), menuliskan deskripsi, "
        "meninjau kembali ringkasan laporan pada halaman Review, dan saat tombol kirim ditekan, sistem menerbitkan Tiket Pelaporan resmi unik dengan format #TK-xxxx.",
        "Demonstrasikan tab 'Scan QR', klik simulasi QR 'KR-A002-07', tunjukkan auto-fill form, pasang foto bukti, dan klik 'Kirim Laporan' hingga muncul halaman sukses tiket #TK-xxxx."
    )
    add_bullet_point("Efisiensi Input", "Auto-fill gedung dan kategori menghemat waktu pelaporan hingga 70% dibanding input manual.")
    add_bullet_point("Multi-format Upload", "Mendukung upload multipart form-data baik dari kamera HP langsung maupun file gambar dari laptop/web.")
    add_bullet_point("Hasil Uji Modul 2", "Tiket laporan langsung diterbitkan dengan status awal 'Diajukan' dan tersimpan di database JSON.")

    # =========================================================================
    # 4. MODUL 3
    # =========================================================================
    add_section_heading("BAGIAN 4: MODUL 3 (MOD-03) — TRACKING STATUS & HISTORI LAPORAN", "Estimasi Waktu: 2 Menit")
    add_speech_bubble(
        "Presenter / Pembicara",
        "Masuk ke Modul 3: Tracking Status dan Histori Laporan Pelapor. Salah satu kelemahan sistem lama adalah mahasiswa tidak pernah tahu nasib laporannya setelah dikirimkan.\n\n"
        "Di Modul 3, mahasiswa memiliki menu 'Laporan Saya' dengan filter status: Semua, Diproses, dan Selesai. "
        "Inovasi visual utama kami adalah widget Vertical Status Timeline Tracker 4 Tahap, yaitu: Diajukan -> Ditinjau Admin -> Diproses -> Selesai.\n\n"
        "Setiap tahap menampilkan indikator warna aktif, tanggal pembaruan status, dan yang paling penting: Catatan Tindak Lanjut dari Petugas. "
        "Mahasiswa bisa membaca langsung misalnya 'Teknisi dijadwalkan Rabu pk 10.00'. Ini mewujudkan transparansi penuh antara pihak kampus dan mahasiswa.",
        "Buka tab 'Laporan Saya' di akun Mahasiswa, klik salah satu tiket (#TK-xxxx), dan tunjukkan alur linimasa vertikal beserta catatan petugas."
    )
    add_bullet_point("Segmentasi Status", "Memisahkan tiket yang baru diajukan, yang sedang ditangani, dan yang telah selesai.")
    add_bullet_point("Transparansi Catatan", "Catatan teknisi tersinkronisasi langsung dari tindakan admin di backend.")

    # =========================================================================
    # 5. MODUL 4
    # =========================================================================
    add_section_heading("BAGIAN 5: MODUL 4 (MOD-04) — DASHBOARD ADMIN & KELOLA TIKET", "Estimasi Waktu: 2.5 Menit")
    add_speech_bubble(
        "Presenter / Pembicara",
        "Sekarang kita beralih ke sisi Administrator, yaitu Modul 4: Dashboard Admin dan Kelola Tiket Perbaikan. "
        "Layar ini dirancang sebagai Command Center bagi biro fasilitas dan logistik kampus.\n\n"
        "Di bagian atas, terdapat 3 kartu ringkasan metrik utama: Berapa tiket yang sedang Diproses, berapa yang sudah Selesai, dan berapa Total Laporan masuk. "
        "Kabar baiknya, kartu-kartu ini interaktif dan dapat diklik! Jika admin mengklik kartu 'Diproses', sistem langsung memfilter dan menampilkan daftar tiket yang sedang dikerjakan. "
        "Begitu juga jika mengklik 'Selesai' atau 'Total'.\n\n"
        "Pada modul ini admin melakukan verifikasi kelayakan: jika laporan valid, admin menekan 'Terima & Jadwalkan Teknisi' (menyimpan data ke tabel TINDAKAN_PENANGANAN dan memicu notifikasi push). "
        "Namun jika laporan tidak valid/duplikat, admin menekan 'Tolak' dengan kewajiban mengisi alasan penolakan agar pelapor mendapat penjelasan logis.",
        "Login sebagai Admin. Klik kartu metrik 'Diproses' atau 'Selesai' untuk menunjukkan filter otomatis, lalu buka satu tiket untuk menunjukkan tombol 'Terima Laporan' dan 'Tolak Laporan'."
    )
    add_bullet_point("Interaktivitas Dashboard", "Klik kartu metrik atau baris kategori langsung menyaring data secara instan.")
    add_bullet_point("Integritas Data", "Penolakan tiket wajib menyertakan alasan penolakan (validasi HTTP 400).")
    add_bullet_point("Relasi Entitas", "Tersimpan lengkap pada tabel TINDAKAN_PENANGANAN di database.")

    # =========================================================================
    # 6. MODUL 5
    # =========================================================================
    add_section_heading("BAGIAN 6: MODUL 5 (MOD-05) — SUBSISTEM ANALYTICS & RANGKUMAN EKSEKUTIF AI", "Estimasi Waktu: 2.5 Menit")
    add_speech_bubble(
        "Presenter / Pembicara",
        "Bapak dan rekan-rekan sekalian, di Modul 5 kita mulai masuk ke ranah kecerdasan buatan, yaitu Subsistem Analytics dan Rangkuman Eksekutif AI.\n\n"
        "Pimpinan biro logistik dan wakil rektor tidak punya waktu membaca puluhan tiket satu per satu. "
        "Melalui Modul 5, kami mengintegrasikan Google Gemini AI SDK untuk menganalisis seluruh data laporan kerusakan secara otomatis.\n\n"
        "Hasil sintesis AI disajikan dalam bentuk Executive Summary Card yang memuat:\n"
        "1. Pola fasilitas paling sering rusak beserta persentasenya (misal: 'Kursi menjadi fasilitas paling sering rusak dengan 36 laporan atau 77%').\n"
        "2. Wilayah gedung dengan kerusakan dominan (misal: 'Gedung A mencatat keluhan tertinggi').\n"
        "3. Laporan berkeparahan tinggi yang masih menunggu penanganan.\n"
        "4. Serta Rekomendasi Strategis AI, seperti menyarankan pengadaan perbaikan massal atau inspeksi berkala di gedung terkait.",
        "Buka tab 'Rangkum' di navigasi bawah Admin. Pilih filter gedung, lalu tekan tombol 'Rangkum dengan AI'. Tunjukkan hasil 3 bullet point dan rekomendasi strategis AI."
    )
    add_bullet_point("Dual-Engine Architecture", "Tersambung native ke Google Gemini API (gemini-2.5-flash) dengan fallback statistik empiris yang cerdas dan bebas kuota.")
    add_bullet_point("Filter Fleksibel", "Dapat menyaring rangkuman per gedung spesifik maupun periode bulanan.")

    # =========================================================================
    # 7. MODUL 6
    # =========================================================================
    add_section_heading("BAGIAN 7: MODUL 6 (MOD-06) — ENGINE PRIORITASI & SCORING PENANGANAN AI", "Estimasi Waktu: 3 Menit")
    add_speech_bubble(
        "Presenter / Pembicara",
        "Dan modul puncak yang menyempurnakan sistem ini adalah Modul 6: Engine Prioritasi dan Scoring Penanganan AI.\n\n"
        "Di lapangan, teknisi fasilitas memiliki keterbatasan personel. Jika menggunakan antrean biasa (first-come first-served), "
        "bisa saja kursi goyang diperbaiki lebih dulu daripada AC laboratorium atau proyektor ruang ujian yang rusak parah. Ini tentu tidak efisien.\n\n"
        "Di Modul 6, kami menciptakan Formula Matematis Skor Urgensi (0–100) komposit 3 variabel dengan bobot objektif:\n"
        "• Keparahan Laporan (Bobot 40%): Berat bernilai 100, Sedang 60, Ringan 30.\n"
        "• Frekuensi Kerusakan Aset/Gedung (Bobot 30%): Dihitung dari akumulasi laporan berulang pada aset atau gedung yang sama.\n"
        "• Dampak Fasilitas terhadap Kegiatan Kampus (Bobot 30%): Fasilitas vital seperti kelistrikan, AC lab, dan proyektor bernilai 95-100, sedangkan fasilitas penunjang bernilai 50-75.\n\n"
        "Skor akhir dikelompokkan ke dalam 3 kategori warna tegas:\n"
        "• Prioritas Tinggi (Skor > 80, Aksen Merah): Penanganan darurat 1x24 jam.\n"
        "• Prioritas Sedang (Skor 50-80, Aksen Kuning/Oranye): Penanganan 2-3 hari kerja.\n"
        "• Prioritas Rendah (Skor < 50, Aksen Hijau): Masuk jadwal pemeliharaan mingguan.",
        "Buka tab 'Prioritas' di navigasi Admin. Tunjukkan daftar tiket terurut dari Rank #1. Klik tombol 'Rincian Skor' untuk menunjukkan breakdown matematis 40%/30%/30%, lalu tunjukkan tombol 'Tindak Lanjuti'."
    )
    add_bullet_point("Perangkingan Otomatis", "Tiket otomatis diurutkan dari skor urgensi tertinggi (Rank #1, #2, dst.).")
    add_bullet_point("Transparansi Matematis", "Modal bottom sheet menampilkan breakdown lengkap penambahan poin subskor (+40 keparahan, +12 frekuensi, +30 dampak = 82 poin).")
    add_bullet_point("Tersinkronisasi ke Database", "Hasil scoring tersimpan di tabel ANALISIS_AI dengan jenis 'PRIORITAS_SKOR' dan mengupdate record laporan.")

    # =========================================================================
    # 8. KESIMPULAN & SESI TANYA JAWAB
    # =========================================================================
    add_section_heading("BAGIAN 8: KESIMPULAN & PERSIAPAN TANYA JAWAB (Q&A)", "Estimasi Waktu: 2 Menit")
    add_speech_bubble(
        "Presenter / Pembicara",
        "Sebagai kesimpulan, keenam modul yang telah kami bangun berhasil mentransformasi tata kelola pelaporan fasilitas kampus dari yang sebelumnya lambat, parsial, dan manual, "
        "menjadi sistem yang cerdas, transparan, terintegrasi, dan berbasis data ilmiah.\n\n"
        "Seluruh kode program telah diuji dengan unit test otomatis di backend dan lolos 100% tanpa error, "
        "serta kode Dart Flutter bersih dari syntax error. Sistem ini siap diimplementasikan dan dikembangkan lebih lanjut di lingkungan kampus kita.\n\n"
        "Demikian presentasi dari kelompok kami. Kami sangat terbuka untuk menerima pertanyaan, saran, maupun masukan dari Bapak Mansyur. Terima kasih banyak.",
        "Buka sesi tanya jawab dengan percaya diri."
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Tabel Tanya Jawab
    faq_title = doc.add_paragraph()
    r_faq = faq_title.add_run("📋 PANDUAN MENJAWAB PERTANYAAN KRUSIAL DOSEN (FAQ PRESENTASI):")
    r_faq.font.bold = True
    r_faq.font.size = Pt(11)
    r_faq.font.color.rgb = PRIMARY

    faq_table = doc.add_table(rows=5, cols=2)
    faq_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    faqs = [
        ("Bagaimana jika internet mati saat memanggil AI Gemini?", 
         "Sistem kami dilengkapi Dual-Engine Architecture dengan Smart Heuristic Engine. Jika API Key kosong atau offline, sistem otomatis menghitung statistik riil data JSON sehingga aplikasi tetap berfungsi 100% dan tidak pernah crash."),
        ("Mengapa menggunakan JSON database bukan MySQL/PostgreSQL?", 
         "Database file JSON terstruktur sangat ringan, cepat diinisialisasi untuk lingkungan pengembangan agile, mudah diaudit, dan secara struktur tabel relasinya (ERD) telah memetakan 7 entitas utama persis seperti standar database relasional."),
        ("Bagaimana cara kerja formula Modul 6 menjamin objektivitas?", 
         "Formula Urgensi menggunakan komposit 3 variabel independen: Keparahan (40%), Frekuensi Kerusakan Berulang (30%), dan Dampak Fasilitas terhadap KBM (30%). Formula ini menghilangkan bias subjektif petugas saat menentukan tiket prioritas."),
        ("Apakah aplikasi bisa langsung dipasang di smartphone Android?", 
         "Tentu saja. Proyek ini dibangun dengan Flutter multiplatform. Kita dapat menjalankan 'flutter build apk --debug' untuk menghasilkan file installer .apk yang bisa langsung dipasang di HP Android pengguna.")
    ]
    for i, (q, a) in enumerate(faqs):
        row = faq_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_background(c0, "FEF3C7")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0)
        set_cell_margins(c1)
        rq = c0.paragraphs[0].add_run(f"❓ {q}")
        rq.font.bold = True
        rq.font.size = Pt(9.5)
        rq.font.color.rgb = AMBER
        ra = c1.paragraphs[0].add_run(f"💡 Jawaban Tim:\n{a}")
        ra.font.size = Pt(9.5)
        ra.font.color.rgb = TEXT_DARK

    output_path = "Naskah_Presentasi_6_Modul_Aplikasi_Pelaporan_Fasilitas_Kampus.docx"
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    create_document()
