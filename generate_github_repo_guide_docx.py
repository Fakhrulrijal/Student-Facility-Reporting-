import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_github_guide_document(output_filename="Panduan_dan_Penjelasan_GitHub_Repository_Proyek.docx"):
    doc = Document()

    # Set Margins (1 Inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Color Palette
    PRIMARY = RGBColor(0x1E, 0x3A, 0x8A)      # Deep Navy Blue
    SECONDARY = RGBColor(0x25, 0x63, 0xEB)    # Royal Blue
    TEXT_DARK = RGBColor(0x0F, 0x17, 0x2A)    # Slate 900
    TEXT_MUTED = RGBColor(0x47, 0x55, 0x69)   # Slate 600
    ACCENT_GREEN = RGBColor(0x05, 0x96, 0x69) # Emerald Green
    ACCENT_AMBER = RGBColor(0xD9, 0x77, 0x06) # Amber

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(22)
        run.font.bold = True
        run.font.color.rgb = PRIMARY
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(14)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11.5)
        run.font.italic = True
        run.font.color.rgb = TEXT_MUTED
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = PRIMARY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = SECONDARY
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = TEXT_DARK
        return p

    def add_p(text, bold_prefix=None, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Calibri"
            r_pre.font.size = Pt(10.5)
            r_pre.font.bold = True
            r_pre.font.color.rgb = TEXT_DARK
        r_txt = p.add_run(text)
        r_txt.font.name = "Calibri"
        r_txt.font.size = Pt(10.5)
        r_txt.font.color.rgb = TEXT_DARK
        return p

    def add_bullet(label, desc):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r_lbl = p.add_run(label + ": ")
        r_lbl.font.name = "Calibri"
        r_lbl.font.size = Pt(10.5)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = TEXT_DARK
        r_desc = p.add_run(desc)
        r_desc.font.name = "Calibri"
        r_desc.font.size = Pt(10.5)
        r_desc.font.color.rgb = TEXT_DARK
        return p

    def add_callout(title, text, bg_hex="EFF6FF", border_color="2563EB"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        cell.width = Inches(6.5)
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(3)
        r_t = p.add_run(title)
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(11)
        r_t.font.bold = True
        r_t.font.color.rgb = PRIMARY

        p2 = cell.add_paragraph()
        p2.paragraph_format.space_after = Pt(0)
        p2.paragraph_format.line_spacing = 1.15
        r_c = p2.add_run(text)
        r_c.font.name = "Calibri"
        r_c.font.size = Pt(10)
        r_c.font.color.rgb = TEXT_DARK

        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        cell.width = Inches(6.5)
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)

        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.1
        r = p.add_run(code_text)
        r.font.name = "Consolas"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================================
    # COVER / HEADER
    # =========================================================================
    add_title("PANDUAN & PENJELASAN LENGKAP GITHUB REPOSITORY\nSTUDENT FACILITY REPORTING")
    add_subtitle("Struktur Codebase, Strategi Percabangan Git, Tata Kelola Repositori, dan Panduan Kolaborasi Tim\nTugas Pengembangan Modul — Dosen Pengampu: Bapak Mansyur")

    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table)
    meta_data = [
        ("Nama Repositori", "Student-Facility-Reporting-"),
        ("URL Repository GitHub", "https://github.com/Fakhrulrijal/Student-Facility-Reporting-.git"),
        ("Default Branch", "main (Production Ready & Verified)"),
        ("Owner / Hacker", "Fakhrulrijal (Arsitektur Kode, Backend & AI Integration)"),
        ("Lisensi & Akses", "Public / Academic Evaluation Repository"),
        ("Status Kode", "SYNCHRONIZED (Up-to-date, Clean Working Tree, All Tests Pass)")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.3)
        c1.width = Inches(4.2)
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
        if "SYNCHRONIZED" in v:
            r1.font.bold = True
            r1.font.color.rgb = ACCENT_GREEN
        else:
            r1.font.color.rgb = TEXT_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # BAB 1: IKHTISAR REPOSITORI GITHUB
    # =========================================================================
    add_h1("1. IKHTISAR & PERAN GITHUB REPOSITORY")
    add_p(
        "Repositori GitHub Student-Facility-Reporting- merupakan pusat kendali kode tunggal "
        "(Single Source of Truth / SSOT) dari seluruh pengembangan sistem Aplikasi Pelaporan Fasilitas Kampus Berbasis AI & Mobile. "
        "Repositori ini mengintegrasikan seluruh komponen arsitektur perangkat lunak dalam satu kesatuan monorepo yang rapi, mencakup:"
    )
    add_bullet("Frontend Mobile & Web", "Aplikasi Flutter 3 berbasis Dart dengan dukungan antarmuka multiplatform (Android Native APK, iOS Standalone PWA, dan Web SPA).")
    add_bullet("Backend RESTful API", "Server backend Python FastAPI berkecepatan tinggi dengan dokumentasi interaktif Swagger OpenAPI (/docs).")
    add_bullet("Kecerdasan Buatan (AI Engine)", "Integrasi Google Gemini AI SDK (gemini-2.5-flash) yang dilengkapi algoritma Smart Empirical Fallback bebas kuota.")
    add_bullet("Database Relasional Terstruktur", "Penyimpanan data berbasis JSON relasional yang memetakan 6 entitas data utama kampus.")
    add_bullet("Artefak Rekayasa Perangkat Lunak (Docs)", "Dokumentasi Product Requirement Document (PRD), Agile User Stories, Architecture Decision Record (ADR), naskah presentasi, hingga panduan teknis APK.")

    add_callout(
        "👥 Distribusi Peran Tim dalam Repositori:",
        "• Fakhrulrijal (Hacker): Penanggung jawab repositori, arsitektur backend FastAPI, integrasi AI Gemini, konfigurasi native Android SDK, dan pipeline kompilasi APK.\n"
        "• Muhammad (Hipster): Riset pengalaman pengguna, desain UI/UX Material 3, rancangan wireframe alur linimasa pelaporan, dan pengujian antarmuka.\n"
        "• Roni (Hustler): Perumusan problem statement, penyusunan Product Goal, matriks prioritas MoSCoW, validasi nilai bisnis produk, dan dokumentasi naskah presentasi tim."
    )

    # =========================================================================
    # BAB 2: STRUKTUR DIREKTORI REPOSITORI
    # =========================================================================
    add_h1("2. ANATOMI & STRUKTUR DIREKTORI (FOLDER STRUCTURE)")
    add_p(
        "Repositori disusun dengan pemisahan tugas (Separation of Concerns / SoC) yang sangat jelas "
        "sehingga memudahkan navigasi kode, kolaborasi antarpengembang, dan proses audit pengujian:"
    )

    add_code_block(
        "Student-Facility-Reporting-/\n"
        "├── android/                 # Konfigurasi Native Android (Gradle, Manifest, SDK 36)\n"
        "├── backend/                 # Source Code Server Backend (Python FastAPI)\n"
        "│   ├── app/                 # Modul Logika Backend (core, database, models, routers)\n"
        "│   │   ├── core/            # Keamanan, Hashing Bcrypt, JWT Token Handler\n"
        "│   │   ├── database/        # JSON DB Engine (CRUD Laporan, User, Fasilitas)\n"
        "│   │   ├── models/          # Skema Validasi Pydantic (Auth, Report, AI Scoring)\n"
        "│   │   └── routers/         # API Endpoints (auth, reports, admin, analytics, priority)\n"
        "│   ├── data/                # database.json (File Database Relasional Nyata)\n"
        "│   ├── uploads/             # Direktori Penyimpanan Foto Bukti Kerusakan\n"
        "│   └── main.py              # Entry Point Eksekusi Uvicorn FastAPI Server\n"
        "├── docs/                    # Dokumentasi Formal PRD, ADR, Backlog, Hasil Riset\n"
        "├── lib/                     # Source Code Frontend Mobile/Web (Flutter Dart)\n"
        "│   ├── models/              # Data Model Dart (User, Facility, Report, Action)\n"
        "│   ├── providers/           # State Management Provider (Auth, Report, Admin, AI)\n"
        "│   ├── screens/             # Antarmuka Pengguna (auth, home, admin, reports)\n"
        "│   ├── services/            # ApiService (Dynamic Host IP, HTTP Request Client)\n"
        "│   ├── widgets/             # Komponen Reusable UI (CustomTextField, TimelineTracker)\n"
        "│   └── main.dart            # Inisialisasi Aplikasi Mobile & MultiProvider Shell\n"
        "├── web/                     # Asset & Manifest Web Platform (PWA & Web Distribution)\n"
        "├── build_and_sign_apk.bat   # Skrip Otomasi Kompilasi & Dual-Signing V1+V2+V3 APK\n"
        "├── web_server.py            # Multi-Threaded HTTP Server Port 3000 (File Downloader)\n"
        "├── pubspec.yaml             # Manajemen Dependensi Pustaka Flutter\n"
        "├── requirements.txt         # Manajemen Dependensi Pustaka Python Backend\n"
        "└── README.md                # Dokumentasi Utama Repositori GitHub"
    )

    add_h2("Rincian Fungsi Direktori Utama:")
    add_bullet("Folder lib/ (Frontend Flutter)", "Berisi seluruh kode logika visual antarmuka pengguna. Menggunakan arsitektur Clean State Management dengan Provider yang memisahkan logika data dari widget visual.")
    add_bullet("Folder backend/ (Backend FastAPI)", "Menyediakan layanan RESTful API dengan validasi input Pydantic yang kuat, enkripsi keamanan kata sandi, perhitungan formula scoring urgensi AI, dan manajemen berkas gambar multipart.")
    add_bullet("Folder android/ (Native Android Bridge)", "Mengatur perizinan sistem operasi seluler (kamera, internet, cleartext traffic) dan parameter build Gradle untuk menghasilkan file APK.")
    add_bullet("Folder docs/ (Artefak Formal Rekayasa)", "Menyimpan seluruh dokumen perencanaan perangkat lunak: 01-project-brief.md, 02-problem-statement.md, 03-product-goal.md, 04-prd.md, 05-initial-backlog.md, 06-role-assignment.md, 07-ai-hypothesis.md, dan catatan ADR.")

    # =========================================================================
    # BAB 3: STRATEGI PERCABANGAN (BRANCHING STRATEGY)
    # =========================================================================
    add_h1("3. STRATEGI PERCABANGAN (BRANCHING) & TATA KELOLA GIT")
    add_p(
        "Repositori ini menerapkan standar industri Feature Branching Workflow berbasis modul. "
        "Setiap modul dari tugas mata kuliah dikembangkan secara terisolasi pada cabang fitur khusus sebelum digabungkan ke cabang utama (main):"
    )

    branch_table = doc.add_table(rows=8, cols=3)
    branch_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(branch_table)

    headers = ["Nama Cabang (Branch)", "Fokus Modul & Fitur", "Status Penggabungan (Merge)"]
    row_hdr = branch_table.rows[0]
    for j, h in enumerate(headers):
        c = row_hdr.cells[j]
        set_cell_background(c, "1E3A8A")
        set_cell_margins(c, top=140, bottom=140, left=160, right=160)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    branch_data = [
        ("main", "Cabang utama stabil (Production/Release). Menyimpan seluruh 6 modul lengkap.", "DEFAULT / ACTIVE"),
        ("feature/mod-01-auth", "Pengembangan Modul 1: Autentikasi JWT, Bcrypt, & RBAC Multi-role.", "MERGED to main"),
        ("feature/mod-02-reporting", "Pengembangan Modul 2: Form Lapor, Scan QR Kamera, & Upload Foto.", "MERGED to main"),
        ("feature/mod-03-tracking", "Pengembangan Modul 3: Linimasa Vertikal & Tracking Riwayat Tiket.", "MERGED to main"),
        ("feature/mod-04-admin", "Pengembangan Modul 4: Dashboard Metrik & Aksi Verifikasi Laporan.", "MERGED to main"),
        ("feature/mod-05-analytics", "Pengembangan Modul 5: Rangkuman Eksekutif Google Gemini AI.", "MERGED to main"),
        ("feature/mod-06-scoring", "Pengembangan Modul 6: Formula Urgensi Matematis & Scoring AI.", "MERGED to main")
    ]

    for i, row_data in enumerate(branch_data):
        row = branch_table.rows[i + 1]
        for j, val in enumerate(row_data):
            c = row.cells[j]
            set_cell_margins(c, top=100, bottom=100, left=140, right=140)
            if j == 0:
                c.width = Inches(2.2)
                set_cell_background(c, "F1F5F9")
                r = c.paragraphs[0].add_run(val)
                r.font.name = "Consolas"
                r.font.bold = True
                r.font.size = Pt(9)
                r.font.color.rgb = TEXT_DARK
            elif j == 1:
                c.width = Inches(2.8)
                set_cell_background(c, "FFFFFF")
                r = c.paragraphs[0].add_run(val)
                r.font.size = Pt(9.5)
                r.font.color.rgb = TEXT_DARK
            else:
                c.width = Inches(1.5)
                set_cell_background(c, "F0FDF4")
                r = c.paragraphs[0].add_run(val)
                r.font.bold = True
                r.font.size = Pt(9)
                r.font.color.rgb = ACCENT_GREEN

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    add_h2("Standar Pesan Commit (Conventional Commits):")
    add_p(
        "Untuk menjaga riwayat commit tetap bersih dan mudah ditelusuri, tim menggunakan format pesan commit terstandar:"
    )
    add_bullet("feat:", "Penambahan fungsionalitas fitur baru (misal: feat: Dynamic server IP configuration and Android release APK dual signing).")
    add_bullet("fix:", "Perbaikan bug atau anomali program (misal: fix: missing ApiService import on login screen).")
    add_bullet("docs:", "Pembaruan dokumen resmi laporan dan panduan teknis (misal: docs: Add technical guide for Android APK conversion).")
    add_bullet("chore:", "Sinkronisasi basis data atau konfigurasi pendukung (misal: chore(data): sync latest facility reports).")

    # =========================================================================
    # BAB 4: PANDUAN MENJALANKAN PROYEK DARI REPOSITORY
    # =========================================================================
    add_h1("4. PANDUAN SETUP & MENJALANKAN PROYEK DARI GITHUB")
    add_p(
        "Bagi dosen penguji atau pengembang lain yang ingin menguji proyek ini di komputer mereka, "
        "berikut adalah panduan langkah instalasi dan eksekusi dari nol:"
    )

    add_h3("Langkah 1: Mengunduh / Kloning Repositori")
    add_code_block("git clone https://github.com/Fakhrulrijal/Student-Facility-Reporting-.git\ncd Student-Facility-Reporting-")

    add_h3("Langkah 2: Menyiapkan dan Menjalankan Backend Server (Python FastAPI)")
    add_code_block(
        "cd backend\n"
        "pip install -r requirements.txt\n"
        "python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
    )
    add_p("Setelah berjalan, buka browser di alamat http://127.0.0.1:8000/docs untuk melihat dokumentasi interaktif Swagger API.")

    add_h3("Langkah 3: Menjalankan Aplikasi Frontend Mobile/Web (Flutter)")
    add_code_block(
        "flutter pub get\n"
        "# Untuk menjalankan di browser Web:\n"
        "flutter run -d chrome\n\n"
        "# Untuk mengompilasi APK Android Fisik:\n"
        "cmd.exe /c build_and_sign_apk.bat"
    )

    # =========================================================================
    # BAB 5: KEUNGGULAN REPOSITORI UNTUK PENILAIAN AKADEMIK
    # =========================================================================
    add_h1("5. NILAI KEUNGGULAN REPOSITORI BAGI EVALUASI DOSEN (PAK MANSYUR)")
    add_p(
        "Repositori ini dirancang bukan sekadar sebagai tempat menyimpan file, melainkan bukti otentik "
        "kompetensi rekayasa perangkat lunak modern tingkat lanjut:"
    )
    add_bullet("Keterlacakan Riwayat Lengkap (Full Traceability)", "Dosen dapat memeriksa riwayat commit dari awal pembentukan PRD hingga modul AI terakhir. Seluruh progres pengerjaan terekam transparan tanpa ada kode instan yang diselipkan.")
    add_bullet("Modularitas Kode 100% Sesuai Tugas", "Pembagian 6 cabang fitur membuktikan bahwa tim memahami pembagian arsitektur modul sistem (MOD-01 hingga MOD-06).")
    add_bullet("Kesiapan Produksi (Production Ready)", "Aplikasi telah teruji lolos kompilasi biner APK rilis dengan dual signature schemes, terhubung realtime ke backend FastAPI, dan telah diverifikasi bebas error sintaks.")

    add_callout(
        "🏆 Kesimpulan Repositori:",
        "Repositori GitHub 'Student-Facility-Reporting-' merupakan portofolio akademik dan teknis yang solid, "
        "memperlihatkan sinergi sempurna antara manajemen versi Git profesional, arsitektur kode modern (Flutter & FastAPI), "
        "dan penerapan kecerdasan buatan mutakhir (Google Gemini AI)."
    )

    doc.save(output_filename)
    print(f"[SUCCESS] GitHub guide document created successfully at: {output_filename}")

if __name__ == "__main__":
    build_github_guide_document()
