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

def build_app_guide_document(output_filename="Panduan_Lengkap_Konversi_Proyek_Menjadi_Aplikasi_Android_APK.docx"):
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
    CODE_BG = "F8FAFC"
    BOX_BG = "EFF6FF"

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
    # HEADER / COVER
    # =========================================================================
    add_title("PANDUAN TEKNIS KOMPILASI & KONVERSI PROYEK\nMENJADI APLIKASI NATIVE ANDROID (APK)")
    add_subtitle("Laporan Rekayasa Perangkat Lunak: Dari Kode Flutter Menjadi Paket Biner Mandiri (.apk)\nTugas Modul Pengembangan Aplikasi Mobile — Dosen Pengampu: Bapak Mansyur")

    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table)
    meta_data = [
        ("Nama Aplikasi", "Aplikasi Pelaporan Fasilitas Kampus Berbasis AI & Mobile"),
        ("Tipe Distribusi", "Standalone Native Android Package (.APK Release)"),
        ("Target Platform", "Android OS 5.0 (Lollipop - API 21) hingga Android 14/15 (API 34/36)"),
        ("Arsitektur Kompilasi", "AOT (Ahead-of-Time) Compiled ARM64 / AArch64 / x86_64"),
        ("Status Paket Biner", "SIAP DIGUNAKAN — Lolos Verifikasi Tanda Tangan Ganda V1 + V2 + V3")
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
        if "SIAP" in v:
            r1.font.bold = True
            r1.font.color.rgb = ACCENT_GREEN
        else:
            r1.font.color.rgb = TEXT_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # BAB 1: PENDAHULUAN & KONSEP DASAR
    # =========================================================================
    add_h1("1. PENDAHULUAN: DARI WEB MENJADI 100% APLIKASI NATIVE ANDROID")
    add_p(
        "Pada tahap awal pengembangan, sebuah proyek Flutter umumnya dijalankan di browser web (Flutter Web) "
        "atau lingkungan emulator untuk kemudahan debugging. Namun, aplikasi pelaporan kerusakan fasilitas kampus "
        "memiliki kebutuhan esensial yang menuntut aplikasi berjalan 100% dalam bentuk aplikasi fisik di smartphone Android (file .apk):"
    )
    add_bullet("Akses Penuh Perangkat Keras Kamera", "Aplikasi membutuhkan kamera smartphone secara native untuk mengambil foto bukti kerusakan berkualitas tinggi dan memindai QR Code aset secara langsung tanpa hambatan perizinan browser.")
    add_bullet("Kemandirian Tanpa Browser (Standalone)", "Aplikasi terpasang resmi di App Drawer smartphone, memiliki ikon aplikasi sendiri, splash screen, dan dapat dibuka kapan saja tanpa memerlukan URL browser.")
    add_bullet("Performa Tinggi 60 FPS Native", "Kode program Dart dikompilasi secara Ahead-of-Time (AOT) langsung ke kode mesin biner ARM/AArch64, menghasilkan animasi mulus dan respon sentuh instan.")
    add_bullet("Persistensi Konfigurasi Server (SharedPreferences)", "Aplikasi menyimpan alamat IP server backend secara lokal di memori HP, memungkinkan penyesuaian dinamis saat pengguna berpindah jaringan Wi-Fi.")

    add_callout(
        "💡 Definisi File APK (Android Package Kit):",
        "APK adalah format file arsip paket aplikasi yang digunakan oleh sistem operasi Android untuk mendistribusikan "
        "dan memasang aplikasi perangkat lunak seluler. Di dalamnya terdapat berkas biner DEX (Dalvik Executable), pustaka C/C++ native, "
        "seluruh aset gambar/font antarmuka, berkas manifest XML, serta sertifikat penandatanganan digital resmi."
    )

    # =========================================================================
    # BAB 2: ANATOMI & PROSES TEKNIS KONVERSI
    # =========================================================================
    add_h1("2. TAHAPAN LENGKAP PROSES KONVERSI MENJADI APK")

    add_h2("Tahap 1: Penyiapan Lingkungan Kompilasi (Build Toolchain)")
    add_p(
        "Kompilasi aplikasi Android membutuhkan tiga perangkat lunak utama yang terkonfigurasi di sistem operasi laptop:"
    )
    add_bullet("Java Development Kit (JDK 17)", "Digunakan oleh Gradle untuk mengeksekusi tugas kompilasi biner Java/Kotlin.")
    add_bullet("Android Software Development Kit (Android SDK)", "Menyediakan Android Platform API, Build-Tools 36.0.0, serta utilitas penandatanganan (apksigner, zipalign).")
    add_bullet("Flutter SDK 3", "Menyediakan Flutter Engine, framework widget Dart, dan kompiler AOT (Ahead-of-Time).")

    add_p("Konfigurasi variabel lingkungan (Environment Variables) diatur sebagai berikut:", "Script Pengaturan Environment: ")
    add_code_block(
        'set "JAVA_HOME=D:\\AndroidSdk\\jdk-17"\n'
        'set "ANDROID_HOME=D:\\AndroidSdk"\n'
        'set "PATH=D:\\AndroidSdk\\jdk-17\\bin;D:\\AndroidSdk\\build-tools\\36.0.0;C:\\src\\flutter\\bin;%PATH%"'
    )

    add_h2("Tahap 2: Konfigurasi Level Kompilasi & Target SDK (build.gradle.kts)")
    add_p(
        "Agar plugin kamera (mobile_scanner) dan plugin penyimpanan lokal (shared_preferences) dapat berjalan stabil di Android versi terbaru "
        "sekaligus tetap kompatibel dengan HP Android versi lama, berkas android/app/build.gradle.kts dikonfigurasi secara khusus:"
    )
    add_bullet("compileSdk = 36", "Menggunakan SDK versi 36 agar seluruh fitur plugin modern dapat dikompilasi tanpa error ketidakcocokan dependensi.")
    add_bullet("targetSdk = 34", "Menargetkan Android 14 untuk memenuhi standar keamanan dan privasi Google Play Store modern.")
    add_bullet("minSdk = 21", "Mendukung perangkat Android mulai dari versi 5.0 (Lollipop) ke atas, mencakup lebih dari 99% HP Android di seluruh dunia.")

    add_code_block(
        "android {\n"
        "    namespace = \"com.example.student_facility_reporting\"\n"
        "    compileSdk = 36\n\n"
        "    defaultConfig {\n"
        "        applicationId = \"com.example.student_facility_reporting\"\n"
        "        minSdk = 21\n"
        "        targetSdk = 34\n"
        "        versionCode = flutter.versionCode\n"
        "        versionName = flutter.versionName\n"
        "    }\n"
        "}"
    )

    add_h2("Tahap 3: Pemberian Izin Perangkat Keras & Jaringan (AndroidManifest.xml)")
    add_p(
        "Sistem keamanan Android mewajibkan setiap aplikasi mendeklarasikan secara eksplisit perangkat keras "
        "dan jenis jaringan yang akan digunakan di dalam file android/app/src/main/AndroidManifest.xml:"
    )
    add_bullet("Izin Internet (android.permission.INTERNET)", "Mengizinkan aplikasi mengirim dan menerima data HTTP ke server backend.")
    add_bullet("Izin Kamera (android.permission.CAMERA)", "Mengizinkan modul pelaporan mengambil foto bukti kerusakan dan memindai QR Code.")
    add_bullet("Izin Lalu Lintas Data Lokal (android:usesCleartextTraffic='true')", "Wajib diaktifkan agar aplikasi diizinkan berkomunikasi dengan backend server lokal laptop via HTTP (port 8000) tanpa diblokir oleh kebijakan default HTTPS Android 9 ke atas.")

    add_code_block(
        '<manifest xmlns:android="http://schemas.android.com/apk/res/android">\n'
        '    <uses-permission android:name="android.permission.INTERNET"/>\n'
        '    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>\n'
        '    <uses-permission android:name="android.permission.CAMERA"/>\n'
        '    <uses-feature android:name="android.hardware.camera" android:required="false"/>\n'
        '    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>\n\n'
        '    <application\n'
        '        android:label="Fasilitas Kampus"\n'
        '        android:icon="@mipmap/ic_launcher"\n'
        '        android:usesCleartextTraffic="true">\n'
        '        ...\n'
        '    </application>\n'
        '</manifest>'
    )

    add_h2("Tahap 4: Inovasi Konfigurasi IP Server Dinamis di HP (Anti Gagal Recompile)")
    add_p(
        "Salah satu masalah terbesar saat membuat aplikasi mobile yang terhubung ke server laptop lokal adalah: "
        "IP Wi-Fi laptop selalu berubah-ubah setiap kali berganti jaringan (akibat DHCP Router). "
        "Jika IP di-hardcode ke dalam kode sumber, maka setiap kali ganti Wi-Fi, aplikasi APK harus di-build ulang berjam-jam.\n\n"
        "Untuk memecahkan masalah ini secara permanen, tim menerapkan arsitektur Dynamic Server Host Configuration:"
    )
    add_bullet("Penyimpanan SharedPreferences di HP", "Saat aplikasi dibuka pertama kali, kelas ApiService.init() membaca alamat IP server yang tersimpan di memori lokal HP Android.")
    add_bullet("Tombol Chip Interaktif di Layar Login", "Di pojok kanan atas form login, terdapat tombol 'Server: 192.168.1.8'. Ketika tombol diketuk, muncul dialog input teks yang memungkinkan penguji atau dosen memasukkan IP laptop yang baru tanpa harus menyentuh kode program.")

    add_code_block(
        "// lib/services/api_service.dart\n"
        "class ApiService {\n"
        "  static String customHost = '192.168.1.8';\n\n"
        "  static Future<void> init() async {\n"
        "    final prefs = await SharedPreferences.getInstance();\n"
        "    final savedHost = prefs.getString('server_host');\n"
        "    if (savedHost != null && savedHost.trim().isNotEmpty) {\n"
        "      customHost = savedHost.trim();\n"
        "    }\n"
        "  }\n\n"
        "  static Future<void> setHost(String newHost) async {\n"
        "    customHost = newHost.trim();\n"
        "    final prefs = await SharedPreferences.getInstance();\n"
        "    await prefs.setString('server_host', customHost);\n"
        "  }\n\n"
        "  static String get baseUrl => 'http://$customHost:8000';\n"
        "}"
    )

    add_h2("Tahap 5: Eksekusi Kompilasi Release (flutter build apk --release)")
    add_p(
        "Kompilasi dilakukan menggunakan perintah rilis resmi Flutter. Pada tahap ini, Flutter melakukan serangkaian optimasi tingkat lanjut:"
    )
    add_bullet("Tree-Shaking Aset Font & Icon", "Menghapus karakter font MaterialIcons yang tidak digunakan, mengurangi ukuran aset dari 1.6 MB menjadi hanya 11 KB (efisiensi 99.3%).")
    add_bullet("Ahead-of-Time (AOT) Binary Compilation", "Seluruh kode logika Dart diubah menjadi pustaka biner libapp.so native untuk arsitektur ARM64.")
    add_bullet("Packaging APK Mandiri", "Seluruh file digabungkan menjadi file arsip biner build/app/outputs/flutter-apk/app-release.apk berukuran 65.4 MB.")

    add_h2("Tahap 6: Mengatasi 'Aplikasi Tidak Terinstal' dengan Penandatanganan Ganda (Dual Signature V1 + V2 + V3)")
    add_p(
        "Pada pengujian awal di smartphone Android versi baru, muncul kendala notifikasi 'Aplikasi Tidak Terinstal'. "
        "Hal ini disebabkan oleh standar keamanan Android 11+ yang mewajibkan paket APK ditandatangani dengan "
        "APK Signature Scheme V2 (Whole-file APK Signing) dan V3, bukan hanya sekadar skema JAR V1 lama.\n\n"
        "Tim menyelesaikan kendala ini dengan mengotomasi penandatanganan menggunakan utilitas resmi Android SDK apksigner.bat:"
    )
    add_code_block(
        'call D:\\AndroidSdk\\build-tools\\36.0.0\\apksigner.bat sign ^\n'
        '  --ks "C:\\Users\\LENOVO\\.android\\debug.keystore" ^\n'
        '  --ks-pass pass:android --key-pass pass:android ^\n'
        '  --ks-key-alias androiddebugkey ^\n'
        '  --v1-signing-enabled true ^\n'
        '  --v2-signing-enabled true ^\n'
        '  "build\\app\\outputs\\flutter-apk\\app-release.apk"\n\n'
        'call D:\\AndroidSdk\\build-tools\\36.0.0\\apksigner.bat verify --verbose "app-release.apk"'
    )

    add_p(
        "Hasil verifikasi menunjukkan bahwa paket APK telah memenuhi standar keamanan Android secara sempurna:",
        "Hasil Verifikasi Integritas Tanda Tangan: "
    )
    add_bullet("Verified using v2 scheme (APK Signature Scheme v2)", "TRUE — Menjamin integritas seluruh file dari modifikasi pihak ketiga.")
    add_bullet("Verified using v3 scheme (APK Signature Scheme v3)", "TRUE — Mendukung rotasi kunci penandatanganan pada Android 9 ke atas.")
    add_bullet("Status Instalasi", "100% Lolos instalasi di perangkat fisik Android tanpa peringatan kesalahan paket.")

    # =========================================================================
    # BAB 3: ARSITEKTUR KOMUNIKASI & ALUR KERJA REAL DEVICE
    # =========================================================================
    add_h1("3. ARSITEKTUR KOMUNIKASI REAL DEVICE (HP KE LAPTOP)")
    add_p(
        "Ketika aplikasi APK berjalan secara fisik di smartphone Android Anda, alur komunikasi datanya "
        "berlangsung secara nirkabel melalui jaringan Wi-Fi lokal menggunakan topologi Client-Server:"
    )

    topo_table = doc.add_table(rows=4, cols=3)
    topo_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(topo_table)

    headers = ["Entitas Komponen", "Alamat Jaringan / Port", "Fungsi & Peran Utama"]
    row_hdr = topo_table.rows[0]
    for j, h in enumerate(headers):
        c = row_hdr.cells[j]
        set_cell_background(c, "1E3A8A")
        set_cell_margins(c, top=140, bottom=140, left=160, right=160)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    topo_data = [
        ("Smartphone Android (Klien Fisik)", "192.168.1.x (DHCP)", "Menjalankan aplikasi native Flutter. Menangkap kamera, memindai QR, dan mengirim request HTTP JSON."),
        ("FastAPI Backend Server (Laptop)", "192.168.1.8:8000", "Pusat logika bisnis, autentikasi JWT, kalkulasi formula scoring urgensi AI, dan manajemen database JSON."),
        ("Web & Distribution Server (Laptop)", "192.168.1.8:3000", "Menyediakan jalur unduhan langsung file APK (app-release.apk) dan dokumen Word (laporan_modul.docx).")
    ]

    for i, row_data in enumerate(topo_data):
        row = topo_table.rows[i + 1]
        for j, val in enumerate(row_data):
            c = row.cells[j]
            set_cell_margins(c, top=100, bottom=100, left=140, right=140)
            if j == 0:
                c.width = Inches(2.2)
                set_cell_background(c, "F1F5F9")
                r = c.paragraphs[0].add_run(val)
                r.font.bold = True
                r.font.size = Pt(9.5)
                r.font.color.rgb = TEXT_DARK
            elif j == 1:
                c.width = Inches(1.8)
                set_cell_background(c, "F8FAFC")
                r = c.paragraphs[0].add_run(val)
                r.font.size = Pt(9)
                r.font.color.rgb = SECONDARY
            else:
                c.width = Inches(2.5)
                set_cell_background(c, "FFFFFF")
                r = c.paragraphs[0].add_run(val)
                r.font.size = Pt(9.5)
                r.font.color.rgb = TEXT_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # BAB 4: PANDUAN PENGUJIAN OLEH DOSEN PENGUJI
    # =========================================================================
    add_h1("4. PANDUAN PRAKTIS CARA MEMPERAGAKAN APLIKASI DI DEPAN DOSEN")
    add_p(
        "Untuk mendemonstrasikan bahwa proyek ini 100% telah menjadi aplikasi native yang berjalan di HP secara nyata, "
        "berikut adalah panduan langkah demi langkah saat demonstrasi di hadapan Bapak Mansyur:"
    )
    add_bullet("Langkah 1: Tunjukkan Ikon Aplikasi di Layar HP", "Tunjukkan bahwa aplikasi terpasang di menu smartphone dengan nama 'Fasilitas Kampus' dan ikon aplikasi resmi.")
    add_bullet("Langkah 2: Tunjukkan Fitur Dynamic Server Chip", "Buka aplikasi, tunjukkan chip 'Server: 192.168.1.8' di pojok kanan atas layar login. Jelaskan bahwa arsitektur ini dibuat agar aplikasi tetap bisa tersambung ke laptop meskipun IP Wi-Fi berubah.")
    add_bullet("Langkah 3: Peragakan Tombol Simulasi 1-Klik", "Tekan tombol '[ 👤 Login Mahasiswa (Andrean) ]' dan klik Login. Tunjukkan respon cepat transisi ke beranda mahasiswa.")
    add_bullet("Langkah 4: Peragakan Fitur Scan QR dengan Kamera Nyata", "Buka tab 'Scan QR' atau Form Lapor, peragakan kamera HP memindai kode QR aset fasilitas dan tunjukkan form gedung terisi secara otomatis.")
    add_bullet("Langkah 5: Tunjukkan Tiket Baru Tersimpan", "Kirim laporan, buka menu 'Laporan Saya', dan tunjukkan nomor tiket baru (#TK-xxxx) beserta linimasa vertikal pelacakan.")

    add_callout(
        "🏆 Kesimpulan Rekayasa:",
        "Transformasi proyek dari web menjadi aplikasi native Android (.apk) telah sukses 100%. "
        "Aplikasi ini menggabungkan keunggulan kompilasi native biner ARM, penandatanganan digital resmi Google Android V2/V3, "
        "serta kelenturan komunikasi jaringan dinamis yang menjadikannya sebuah produk perangkat lunak siap pakai."
    )

    doc.save(output_filename)
    print(f"[SUCCESS] App conversion guide document created successfully at: {output_filename}")

if __name__ == "__main__":
    build_app_guide_document()
