import os
import sys
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Direktori Output
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
MOCKUP_DIR = os.path.join(OUTPUT_DIR, "mockup_images")
PDF_PATH = os.path.join(OUTPUT_DIR, "Dokumentasi_Mockup_UI_Aplikasi_Pelaporan_Fasilitas_Kampus.pdf")
os.makedirs(MOCKUP_DIR, exist_ok=True)

# Font paths
FONT_REGULAR = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_SEMIBOLD = r"C:\Windows\Fonts\segoeuisl.ttf"

def get_font(size, bold=False):
    try:
        path = FONT_BOLD if bold else FONT_REGULAR
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

# Palet Warna Mockup (Hex)
BG_LIGHT = "#F8FAFC"
SURFACE = "#FFFFFF"
PRIMARY_NAVY = "#1E3A8A"
SECONDARY_BLUE = "#3B82F6"
ACCENT_CYAN = "#0EA5E9"
TEXT_DARK = "#0F172A"
TEXT_MUTED = "#64748B"
BORDER_COLOR = "#E2E8F0"
SUCCESS_GREEN = "#16A34A"
WARNING_AMBER = "#D97706"
DANGER_RED = "#DC2626"
PURPLE_AI = "#7C3AED"

def create_phone_frame(title="Layar", width=400, height=800):
    """Membuat frame smartphone modern lengkap dengan notch dan status bar."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Chassis Body Smartphone (Rounded Rectangle)
    draw.rounded_rectangle([(10, 10), (width - 10, height - 10)], radius=32, fill=SURFACE, outline="#CBD5E1", width=3)
    
    # Layar Utama (Screen Area)
    # Status bar top
    draw.rectangle([(13, 13), (width - 13, 50)], fill=SURFACE)
    
    # Speaker / Dynamic Notch
    draw.rounded_rectangle([(width // 2 - 50, 16), (width // 2 + 50, 26)], radius=5, fill="#0F172A")
    # Camera dot
    draw.ellipse([(width // 2 + 35, 18), (width // 2 + 41, 24)], fill="#1E293B")
    
    # Status Bar Icons / Jam
    font_clock = get_font(12, bold=True)
    draw.text((32, 22), "09:41", fill=TEXT_DARK, font=font_clock)
    
    # Wi-Fi & Battery indicator
    font_icons = get_font(11, bold=True)
    draw.text((width - 65, 22), "LTE 98%", fill=TEXT_MUTED, font=font_icons)

    # Home bar bottom
    draw.rounded_rectangle([(width // 2 - 45, height - 20), (width // 2 + 45, height - 16)], radius=2, fill="#94A3B8")

    return img, draw

# ==============================================================================
# 1. MOCKUP MOD-01: LOGIN SCREEN
# ==============================================================================
def generate_mockup_01():
    img, draw = create_phone_frame(width=400, height=800)

    # Logo Header Container
    draw.ellipse([(160, 80), (240, 160)], fill="#EFF6FF", outline=SECONDARY_BLUE, width=2)
    font_logo = get_font(30, bold=True)
    draw.text((182, 98), "🏛️", fill=PRIMARY_NAVY, font=font_logo)

    # Title & Subtitle
    font_title = get_font(20, bold=True)
    draw.text((80, 180), "Fasilitas Kampus", fill=PRIMARY_NAVY, font=font_title)
    font_sub = get_font(11)
    draw.text((95, 210), "Sistem Pelaporan Terpadu & AI", fill=TEXT_MUTED, font=font_sub)

    # Role Selector Tabs
    draw.rounded_rectangle([(40, 245), (360, 280)], radius=8, fill="#F1F5F9")
    draw.rounded_rectangle([(42, 247), (198, 278)], radius=6, fill=PRIMARY_NAVY)
    font_role = get_font(12, bold=True)
    draw.text((85, 255), "Mahasiswa", fill=SURFACE, font=font_role)
    draw.text((245, 255), "Admin", fill=TEXT_MUTED, font=font_role)

    # Form Field 1: Email / NIM
    font_lbl = get_font(11, bold=True)
    draw.text((40, 300), "Nomor Induk Mahasiswa (NIM)", fill=TEXT_DARK, font=font_lbl)
    draw.rounded_rectangle([(40, 320), (360, 360)], radius=8, fill=SURFACE, outline=BORDER_COLOR, width=1)
    font_val = get_font(12)
    draw.text((55, 332), "2024010048", fill=TEXT_DARK, font=font_val)

    # Form Field 2: Kata Sandi
    draw.text((40, 375), "Kata Sandi", fill=TEXT_DARK, font=font_lbl)
    draw.rounded_rectangle([(40, 395), (360, 435)], radius=8, fill=SURFACE, outline=BORDER_COLOR, width=1)
    draw.text((55, 407), "••••••••••••", fill=TEXT_DARK, font=font_val)
    draw.text((325, 406), "👁️", fill=TEXT_MUTED, font=font_val)

    # Lupa Password
    draw.text((255, 445), "Lupa Password?", fill=SECONDARY_BLUE, font=get_font(10))

    # Tombol Masuk
    draw.rounded_rectangle([(40, 480), (360, 525)], radius=10, fill=PRIMARY_NAVY)
    font_btn = get_font(14, bold=True)
    draw.text((155, 493), "Masuk", fill=SURFACE, font=font_btn)

    # SSO Divider
    draw.line([(40, 560), (170, 560)], fill=BORDER_COLOR, width=1)
    draw.text((180, 552), "atau", fill=TEXT_MUTED, font=get_font(11))
    draw.line([(215, 560), (360, 560)], fill=BORDER_COLOR, width=1)

    # Tombol SSO Kampus
    draw.rounded_rectangle([(40, 580), (360, 625)], radius=10, fill=SURFACE, outline=BORDER_COLOR, width=1)
    draw.text((120, 595), "Masuk via Akun Kampus (SSO)", fill=TEXT_DARK, font=get_font(11, bold=True))

    # Register Link
    draw.text((110, 670), "Belum punya akun? ", fill=TEXT_MUTED, font=get_font(11))
    draw.text((225, 670), "Daftar Akun", fill=SECONDARY_BLUE, font=get_font(11, bold=True))

    path = os.path.join(MOCKUP_DIR, "mockup_01_login.png")
    img.save(path)
    return path

# ==============================================================================
# 2. MOCKUP MOD-02: CREATE REPORT SCREEN
# ==============================================================================
def generate_mockup_02():
    img, draw = create_phone_frame(width=400, height=800)

    # Top App Bar
    draw.text((25, 55), "←", fill=TEXT_DARK, font=get_font(18, bold=True))
    draw.text((140, 57), "Buat Laporan", fill=PRIMARY_NAVY, font=get_font(15, bold=True))

    # Tab Foto vs Scan QR
    draw.rounded_rectangle([(30, 95), (370, 130)], radius=8, fill="#F1F5F9")
    draw.rounded_rectangle([(32, 97), (198, 128)], radius=6, fill=PRIMARY_NAVY)
    draw.text((70, 105), "📷 Foto Fisik", fill=SURFACE, font=get_font(11, bold=True))
    draw.text((245, 105), "🔲 Scan QR", fill=TEXT_MUTED, font=get_font(11, bold=True))

    # Area Kamera Container
    draw.rounded_rectangle([(30, 145), (370, 280)], radius=12, fill="#F8FAFC", outline="#93C5FD", width=2)
    # Thumbnail Box
    draw.rounded_rectangle([(140, 170), (260, 230)], radius=8, fill="#DBEAFE")
    draw.text((185, 185), "📷", fill=PRIMARY_NAVY, font=get_font(24))
    draw.text((110, 240), "Ambil Foto Kerusakan Fasilitas", fill=PRIMARY_NAVY, font=get_font(11, bold=True))
    draw.text((120, 258), "Kamera fisik ponsel atau galeri", fill=TEXT_MUTED, font=get_font(9))

    # Input Kategori Kerusakan (Chips)
    draw.text((30, 300), "Kategori Kerusakan Fasilitas", fill=TEXT_DARK, font=get_font(11, bold=True))
    categories = [("Kursi", True), ("Proyektor", False), ("AC/Lampu", False), ("DLL", False)]
    cx = 30
    for cat, active in categories:
        bg = PRIMARY_NAVY if active else "#F1F5F9"
        tc = SURFACE if active else TEXT_MUTED
        draw.rounded_rectangle([(cx, 320), (cx + 75, 350)], radius=15, fill=bg)
        draw.text((cx + 18, 328), cat, fill=tc, font=get_font(10, bold=True))
        cx += 85

    # Input Lokasi & Ruangan
    draw.text((30, 370), "Lokasi Gedung & Ruangan", fill=TEXT_DARK, font=get_font(11, bold=True))
    draw.rounded_rectangle([(30, 390), (370, 428)], radius=8, fill=SURFACE, outline=BORDER_COLOR, width=1)
    draw.text((45, 401), "Gedung A • Lantai 3 • Ruang 301", fill=TEXT_DARK, font=get_font(11))
    draw.text((345, 400), "▾", fill=TEXT_MUTED, font=get_font(12, bold=True))

    # Input Deskripsi
    draw.text((30, 445), "Deskripsi Kerusakan", fill=TEXT_DARK, font=get_font(11, bold=True))
    draw.rounded_rectangle([(30, 465), (370, 545)], radius=8, fill=SURFACE, outline=BORDER_COLOR, width=1)
    desc_txt = "Sandaran kursi kuliah patah pada bagian engsel\nkanan. Baut pengunci lepas dan berbahaya jika\ndiduduki mahasiswa saat perkuliahan."
    draw.text((42, 475), desc_txt, fill=TEXT_DARK, font=get_font(10))

    # Urgensi Picker
    draw.text((30, 560), "Tingkat Urgensi Dilaporkan", fill=TEXT_DARK, font=get_font(11, bold=True))
    urgencies = [("Rendah", False, "#16A34A"), ("Sedang", False, "#D97706"), ("Tinggi", True, "#DC2626")]
    ux = 30
    for u_label, is_act, u_col in urgencies:
        bg = u_col if is_act else "#F1F5F9"
        tc = SURFACE if is_act else TEXT_MUTED
        draw.rounded_rectangle([(ux, 580), (ux + 105, 615)], radius=8, fill=bg)
        draw.text((ux + 30, 592), u_label, fill=tc, font=get_font(11, bold=True))
        ux += 115

    # Tombol Ajukan Laporan
    draw.rounded_rectangle([(30, 680), (370, 725)], radius=10, fill=PRIMARY_NAVY)
    draw.text((120, 693), "Kirim Laporan Fasilitas ➔", fill=SURFACE, font=get_font(13, bold=True))

    path = os.path.join(MOCKUP_DIR, "mockup_02_reporting.png")
    img.save(path)
    return path

# ==============================================================================
# 3. MOCKUP MOD-03: TRACKING & VERTICAL TIMELINE
# ==============================================================================
def generate_mockup_03():
    img, draw = create_phone_frame(width=400, height=800)

    # Top Bar
    draw.text((25, 55), "←", fill=TEXT_DARK, font=get_font(18, bold=True))
    draw.text((130, 57), "Detail Laporan & Tiket", fill=PRIMARY_NAVY, font=get_font(14, bold=True))

    # Card Informasi Tiket Utama
    draw.rounded_rectangle([(25, 95), (375, 215)], radius=12, fill="#F8FAFC", outline=BORDER_COLOR, width=1)
    # Badge Nomor Tiket & Status
    draw.rounded_rectangle([(40, 110), (120, 132)], radius=6, fill="#DBEAFE")
    draw.text((50, 115), "#TK-0058", fill=PRIMARY_NAVY, font=get_font(10, bold=True))
    draw.rounded_rectangle([(285, 110), (360, 132)], radius=6, fill="#DBEAFE")
    draw.text((298, 115), "Diproses", fill="#1D4ED8", font=get_font(10, bold=True))

    draw.text((40, 142), "Kursi Kuliah Sandaran Patah", fill=TEXT_DARK, font=get_font(13, bold=True))
    draw.text((40, 165), "📍 Gedung A • Lantai 3 • Ruang 301", fill=TEXT_MUTED, font=get_font(10))
    draw.text((40, 185), "🕒 Dilaporkan: 13 Nov 2026, 14:30 WIB", fill=TEXT_MUTED, font=get_font(10))

    # Heading Timeline
    draw.text((25, 235), "Progres Penanganan Fasilitas", fill=PRIMARY_NAVY, font=get_font(12, bold=True))

    # Vertical Stepper Container
    steps = [
        ("1. Laporan Diajukan", "13 Nov, 14:30", "Laporan dan bukti foto berhasil terkirim.", True, True),
        ("2. Evaluasi & Disposisi", "13 Nov, 15:10", "Disetujui Admin. Ditugaskan ke Teknisi Joko.", True, True),
        ("3. Penanganan di Lokasi", "14 Nov, 09:00", "Teknisi sedang mengganti baut & sandaran.", True, False), # Active
        ("4. Selesai Diperbaiki", "Estimasi 15 Nov", "Pengecekan akhir mutu fungsi fasilitas.", False, False)
    ]

    sy = 270
    for idx, (title, waktu, desc, is_done, has_next) in enumerate(steps):
        # Bullet Node
        circle_col = SUCCESS_GREEN if is_done and has_next else (SECONDARY_BLUE if is_done else "#CBD5E1")
        draw.ellipse([(40, sy + 3), (60, sy + 23)], fill=circle_col)
        
        # Icon inside bullet
        icon_txt = "✓" if (is_done and has_next) else ("⚙" if is_done else "○")
        draw.text((46, sy + 4), icon_txt, fill=SURFACE, font=get_font(10, bold=True))

        # Connecting vertical line
        if idx < len(steps) - 1:
            line_col = SUCCESS_GREEN if is_done and has_next else "#E2E8F0"
            draw.line([(50, sy + 25), (50, sy + 75)], fill=line_col, width=2)

        # Texts
        draw.text((75, sy), title, fill=TEXT_DARK, font=get_font(11, bold=True))
        draw.text((270, sy), waktu, fill=TEXT_MUTED, font=get_font(9))
        draw.text((75, sy + 20), desc, fill=TEXT_MUTED, font=get_font(9))

        sy += 75

    # Tombol Hubungi Bantuan
    draw.rounded_rectangle([(25, 680), (375, 725)], radius=10, fill=SURFACE, outline=PRIMARY_NAVY, width=1)
    draw.text((115, 695), "💬 Konfirmasi / Tanya Admin", fill=PRIMARY_NAVY, font=get_font(12, bold=True))

    path = os.path.join(MOCKUP_DIR, "mockup_03_tracking.png")
    img.save(path)
    return path

# ==============================================================================
# 4. MOCKUP MOD-04: ADMIN DASHBOARD & DISPOSITION
# ==============================================================================
def generate_mockup_04():
    img, draw = create_phone_frame(width=400, height=800)

    # Top Bar
    draw.text((25, 55), "🏛️", fill=PRIMARY_NAVY, font=get_font(18))
    draw.text((65, 57), "Dashboard Admin", fill=PRIMARY_NAVY, font=get_font(15, bold=True))
    draw.text((345, 55), "🔄", fill=TEXT_MUTED, font=get_font(16))

    # Metric Cards Row (Clickable KPI)
    # Card 1: Diproses
    draw.rounded_rectangle([(20, 95), (130, 160)], radius=10, fill="#EFF6FF", outline="#BFDBFE", width=1)
    draw.text((65, 105), "6", fill="#1D4ED8", font=get_font(18, bold=True))
    draw.text((45, 135), "Diproses", fill="#1D4ED8", font=get_font(10, bold=True))

    # Card 2: Selesai
    draw.rounded_rectangle([(145, 95), (255, 160)], radius=10, fill="#F0FDF4", outline="#BBF7D0", width=1)
    draw.text((192, 105), "7", fill=SUCCESS_GREEN, font=get_font(18, bold=True))
    draw.text((170, 135), "Selesai", fill=SUCCESS_GREEN, font=get_font(10, bold=True))

    # Card 3: Total
    draw.rounded_rectangle([(270, 95), (380, 160)], radius=10, fill=PRIMARY_NAVY)
    draw.text((312, 105), "48", fill=SURFACE, font=get_font(18, bold=True))
    draw.text((305, 135), "Total", fill="#93C5FD", font=get_font(10, bold=True))

    # Kategori Kerusakan Breakdown
    draw.text((25, 180), "Distribusi Kategori Kerusakan", fill=TEXT_DARK, font=get_font(12, bold=True))
    kategoris = [
        ("🪑 Kursi Kuliah", "37 Tiket (77%)", "#2563EB", 0.77),
        ("📽️ Proyektor", "11 Tiket (23%)", "#7C3AED", 0.23),
        ("💡 Lampu & AC", "0 Tiket (0%)", "#94A3B8", 0.02)
    ]
    ky = 205
    for kname, kcount, kcolor, ratio in kategoris:
        draw.rounded_rectangle([(20, ky), (380, ky + 45)], radius=8, fill=SURFACE, outline=BORDER_COLOR, width=1)
        draw.text((35, ky + 13), kname, fill=TEXT_DARK, font=get_font(11, bold=True))
        draw.text((275, ky + 13), kcount, fill=TEXT_MUTED, font=get_font(10))
        # Mini progress bar
        draw.line([(35, ky + 36), (365, ky + 36)], fill="#E2E8F0", width=3)
        draw.line([(35, ky + 36), (35 + int(330 * ratio), ky + 36)], fill=kcolor, width=3)
        ky += 55

    # Card Disposisi Cepat / Evaluasi Tiket
    draw.text((25, 385), "Evaluasi & Disposisi Tiket Cepat", fill=PRIMARY_NAVY, font=get_font(12, bold=True))
    draw.rounded_rectangle([(20, 410), (380, 580)], radius=10, fill="#F8FAFC", outline="#BFDBFE", width=1)
    
    draw.text((35, 425), "Tiket: #TK-0059 • Kursi Rusak R.204", fill=PRIMARY_NAVY, font=get_font(11, bold=True))
    draw.text((35, 445), "Pelapor: Mahasiswa (2024010048) • Prioritas: Tinggi", fill=TEXT_MUTED, font=get_font(9))

    # Action Buttons: Terima vs Tolak
    draw.rounded_rectangle([(35, 470), (190, 505)], radius=6, fill=SUCCESS_GREEN)
    draw.text((65, 480), "✓ Terima & Jadwalkan", fill=SURFACE, font=get_font(10, bold=True))

    draw.rounded_rectangle([(205, 470), (365, 505)], radius=6, fill=SURFACE, outline=DANGER_RED, width=1)
    draw.text((245, 480), "✕ Tolak Laporan", fill=DANGER_RED, font=get_font(10, bold=True))

    draw.text((35, 520), "Catatan Teknisi: Ditugaskan ke tim perbaikan Gedung A.", fill=TEXT_DARK, font=get_font(9))
    draw.text((35, 545), "SLA Penanganan: Maksimal 2x24 Jam kerja.", fill="#059669", font=get_font(9, bold=True))

    # Bottom Navigation Bar
    draw.rectangle([(13, 715), (387, 785)], fill=SURFACE)
    draw.line([(13, 715), (387, 715)], fill=BORDER_COLOR, width=1)
    
    navs = [("📊", "Dashboard", True), ("📋", "Laporan", False), ("✨", "Rangkuman", False), ("🎯", "Prioritas", False)]
    nx = 35
    for nicon, nlabel, nact in navs:
        ncol = PRIMARY_NAVY if nact else TEXT_MUTED
        draw.text((nx + 10, 725), nicon, fill=ncol, font=get_font(14))
        draw.text((nx, 750), nlabel, fill=ncol, font=get_font(9, bold=nact))
        nx += 95

    path = os.path.join(MOCKUP_DIR, "mockup_04_admin.png")
    img.save(path)
    return path

# ==============================================================================
# 5. MOCKUP MOD-05: AI EXECUTIVE SUMMARY & ANALYTICS
# ==============================================================================
def generate_mockup_05():
    img, draw = create_phone_frame(width=400, height=800)

    # Top Bar
    draw.text((25, 55), "←", fill=TEXT_DARK, font=get_font(18, bold=True))
    draw.text((120, 57), "Rangkuman AI Eksekutif", fill=PRIMARY_NAVY, font=get_font(14, bold=True))

    # Filter Bar
    draw.rounded_rectangle([(25, 95), (190, 125)], radius=6, fill="#F1F5F9")
    draw.text((38, 103), "Periode: Semester Ganjil ▾", fill=TEXT_DARK, font=get_font(9, bold=True))

    draw.rounded_rectangle([(205, 95), (375, 125)], radius=6, fill="#F1F5F9")
    draw.text((225, 103), "Gedung: Semua Gedung ▾", fill=TEXT_DARK, font=get_font(9, bold=True))

    # AI Card Header
    draw.rounded_rectangle([(25, 140), (375, 410)], radius=12, fill=SURFACE, outline="#DDD6FE", width=2)
    # AI Header Banner
    draw.rounded_rectangle([(25, 140), (375, 190)], radius=12, fill="#7C3AED")
    draw.text((45, 153), "✨ Intelijen Kerusakan Kampus (Gemini AI)", fill=SURFACE, font=get_font(12, bold=True))
    draw.text((45, 172), "Analisis komputasi pola kerusakan fasilitas otomatis", fill="#DDD6FE", font=get_font(8))

    # Bullets Analisis
    bullets = [
        "1. Kursi mendominasi 77% kerusakan (37 dari 48 laporan). Kerusakan mayoritas pada engsel sandaran.",
        "2. Gedung A mencatat konsentrasi tertinggi (37 laporan), menjadikannya area fasilitas paling kritis.",
        "3. Terdapat 30 tiket berkategori urgensi Tinggi yang memerlukan disposisi segera dari teknisi."
    ]
    by = 210
    for b in bullets:
        draw.text((40, by), b[:45], fill=TEXT_DARK, font=get_font(10, bold=True))
        draw.text((40, by + 16), b[45:], fill=TEXT_MUTED, font=get_font(9))
        by += 42

    # Kotak Rekomendasi AI
    draw.rounded_rectangle([(25, 425), (375, 540)], radius=10, fill="#FEF3C7", outline="#FDE68A", width=1)
    draw.text((45, 440), "💡 Rekomendasi Kebijakan AI", fill="#B45309", font=get_font(11, bold=True))
    rekom_txt = "Jadwalkan perbaikan kursi massal dan inspeksi\nmenyeluruh di Gedung A. Pertimbangkan pengadaan\nspare-part sandaran kursi dengan spesifikasi lebih kuat\nuntuk menekan keluhan berulang di semester ini."
    draw.text((45, 465), rekom_txt, fill="#92400E", font=get_font(9))

    # Tombol Ekspor Laporan
    draw.rounded_rectangle([(25, 680), (375, 725)], radius=10, fill=PRIMARY_NAVY)
    draw.text((120, 695), "📥 Ekspor Rangkuman (PDF/Word)", fill=SURFACE, font=get_font(11, bold=True))

    path = os.path.join(MOCKUP_DIR, "mockup_05_analytics.png")
    img.save(path)
    return path

# ==============================================================================
# 6. MOCKUP MOD-06: AI SCORING & PRIORITIZATION
# ==============================================================================
def generate_mockup_06():
    img, draw = create_phone_frame(width=400, height=800)

    # Top Bar
    draw.text((25, 55), "←", fill=TEXT_DARK, font=get_font(18, bold=True))
    draw.text((125, 57), "Prioritas Penanganan AI", fill=PRIMARY_NAVY, font=get_font(14, bold=True))

    # Formula Banner
    draw.rounded_rectangle([(25, 95), (375, 145)], radius=8, fill="#EFF6FF", outline="#BFDBFE", width=1)
    draw.text((40, 105), "Formula Komposit Scoring (0 - 100):", fill=PRIMARY_NAVY, font=get_font(9, bold=True))
    draw.text((40, 122), "Skor = 40% Keparahan + 30% Frekuensi + 30% Dampak", fill="#1E40AF", font=get_font(9))

    # Ticket Rank 1 (Prioritas Tinggi)
    draw.rounded_rectangle([(25, 160), (375, 275)], radius=10, fill=SURFACE, outline="#FECACA", width=2)
    # Rank Badge & Score
    draw.rounded_rectangle([(40, 175), (85, 198)], radius=5, fill=DANGER_RED)
    draw.text((50, 180), "RANK 1", fill=SURFACE, font=get_font(9, bold=True))
    
    draw.rounded_rectangle([(300, 175), (360, 200)], radius=6, fill="#FEE2E2")
    draw.text((310, 181), "SKOR 94", fill=DANGER_RED, font=get_font(10, bold=True))

    draw.text((40, 208), "#TK-0058 • Kursi Patah R.301 Gedung A", fill=TEXT_DARK, font=get_font(11, bold=True))
    draw.text((40, 228), "Detail: Keparahan: 36/40 | Frekuensi: 28/30 | Dampak: 30/30", fill=TEXT_MUTED, font=get_font(9))
    
    draw.rounded_rectangle([(40, 248), (145, 268)], radius=4, fill="#DC2626")
    draw.text((48, 252), "Prioritas: TINGGI", fill=SURFACE, font=get_font(8, bold=True))

    # Ticket Rank 2 (Prioritas Tinggi)
    draw.rounded_rectangle([(25, 290), (375, 405)], radius=10, fill=SURFACE, outline="#FECACA", width=1)
    draw.rounded_rectangle([(40, 305), (85, 328)], radius=5, fill=DANGER_RED)
    draw.text((50, 310), "RANK 2", fill=SURFACE, font=get_font(9, bold=True))

    draw.rounded_rectangle([(300, 305), (360, 330)], radius=6, fill="#FEE2E2")
    draw.text((310, 311), "SKOR 86", fill=DANGER_RED, font=get_font(10, bold=True))

    draw.text((40, 338), "#TK-0042 • Proyektor Mati Total R.402", fill=TEXT_DARK, font=get_font(11, bold=True))
    draw.text((40, 358), "Detail: Keparahan: 32/40 | Frekuensi: 24/30 | Dampak: 30/30", fill=TEXT_MUTED, font=get_font(9))
    draw.rounded_rectangle([(40, 378), (145, 398)], radius=4, fill="#DC2626")
    draw.text((48, 382), "Prioritas: TINGGI", fill=SURFACE, font=get_font(8, bold=True))

    # Ticket Rank 3 (Prioritas Sedang)
    draw.rounded_rectangle([(25, 420), (375, 535)], radius=10, fill=SURFACE, outline="#FDE68A", width=1)
    draw.rounded_rectangle([(40, 435), (85, 458)], radius=5, fill=WARNING_AMBER)
    draw.text((50, 440), "RANK 3", fill=SURFACE, font=get_font(9, bold=True))

    draw.rounded_rectangle([(300, 435), (360, 460)], radius=6, fill="#FEF3C7")
    draw.text((310, 441), "SKOR 69", fill=WARNING_AMBER, font=get_font(10, bold=True))

    draw.text((40, 468), "#TK-0015 • Baut Kursi Goyang R.105", fill=TEXT_DARK, font=get_font(11, bold=True))
    draw.text((40, 488), "Detail: Keparahan: 24/40 | Frekuensi: 20/30 | Dampak: 25/30", fill=TEXT_MUTED, font=get_font(9))
    draw.rounded_rectangle([(40, 508), (155, 528)], radius=4, fill=WARNING_AMBER)
    draw.text((48, 512), "Prioritas: SEDANG", fill=SURFACE, font=get_font(8, bold=True))

    # Tombol Eksekusi Disposisi Otomatis
    draw.rounded_rectangle([(25, 680), (375, 725)], radius=10, fill=PRIMARY_NAVY)
    draw.text((110, 695), "⚡ Disposisi Otomatis Sesuai Skor", fill=SURFACE, font=get_font(11, bold=True))

    path = os.path.join(MOCKUP_DIR, "mockup_06_scoring.png")
    img.save(path)
    return path

# ==============================================================================
# REPORTLAB CUSTOM CANVAS DENGAN HEADER & NUMBERING "HALAMAN X DARI Y"
# ==============================================================================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Jangan gambar header/footer di halaman cover (halaman 1)
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Header
        self.drawString(40, 805, "DOKUMENTASI DESAIN MOCKUP & PANDUAN ANTARMUKA APLIKASI (MODUL 1 - 6)")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(40, 798, 555, 798)

        # Running Footer
        self.line(40, 45, 555, 45)
        self.drawString(40, 32, "Sistem Pelaporan Fasilitas Kampus Berbasis AI & Mobile • Tugas Modul Pak Mansyur")
        page_str = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawRightString(555, 32, page_str)
        self.restoreState()

# ==============================================================================
# GENERATOR DOKUMEN PDF
# ==============================================================================
def build_pdf_document():
    # 1. Buat Semua Gambar Mockup Terlebih Dahulu
    print("Membuat gambar mockup smartphone...")
    m1 = generate_mockup_01()
    m2 = generate_mockup_02()
    m3 = generate_mockup_03()
    m4 = generate_mockup_04()
    m5 = generate_mockup_05()
    m6 = generate_mockup_06()
    print("Semua gambar mockup berhasil dibuat.")

    # 2. Setup Dokumen PDF
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#475569"),
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=14,
        spaceAfter=8
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2563EB"),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        leftIndent=12,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E3A8A")
    )

    story = []

    # --------------------------------------------------------------------------
    # HALAMAN 1: COVER ELEGAN
    # --------------------------------------------------------------------------
    story.append(Spacer(1, 40))
    # Accent Banner Bar
    banner_data = [[Paragraph("<b>DOKUMEN SPESIFIKASI DESAIN ANTARMUKA (UI/UX)</b>", ParagraphStyle('Bnr', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#FFFFFF")))]]
    banner_table = Table(banner_data, colWidths=[515], rowHeights=[26])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#1E3A8A")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 25))

    story.append(Paragraph("Aplikasi Pelaporan Fasilitas Kampus<br/>Berbasis Mobile & Artificial Intelligence", title_style))
    story.append(Paragraph("Dokumentasi Komprehensif Desain Mockup, Arsitektur Antarmuka, dan Penjelasan Teknis Interaksi 6 Modul", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceBefore=10, spaceAfter=20))

    # Metadata Proyek Table
    meta_info = [
        [Paragraph("<b>Mata Kuliah / Tugas:</b>", body_style), Paragraph("Tugas Besar Modul Pembelajaran (Pak Mansyur)", body_style)],
        [Paragraph("<b>Cakupan Modul:</b>", body_style), Paragraph("6 Modul (MOD-01 s/d MOD-06 Terintegrasi Penuh)", body_style)],
        [Paragraph("<b>Platform & UI Engine:</b>", body_style), Paragraph("Flutter Mobile (Android/iOS) & Flutter Web Responsive", body_style)],
        [Paragraph("<b>Backend & AI Engine:</b>", body_style), Paragraph("FastAPI (Python 3.14) & Google Gemini 2.5 Flash", body_style)],
        [Paragraph("<b>Arsitektur State:</b>", body_style), Paragraph("Provider Pattern + Single Source of Truth RESTful API", body_style)],
        [Paragraph("<b>Tanggal Rilis Dokumen:</b>", body_style), Paragraph("17 November 2026", body_style)],
    ]
    meta_table = Table(meta_info, colWidths=[150, 365])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 30))
    # Executive Summary Box
    summary_html = """<b>Ringkasan Eksekutif Desain:</b><br/>
    Dokumen ini menyajikan rancangan visual mockup beresolusi tinggi beserta panduan teknis antarmuka untuk seluruh modul pada aplikasi sistem pelaporan fasilitas kampus. Perancangan UI/UX mengadopsi prinsip <i>Human-Centered Design</i>, kecepatan pelaporan di lapangan (<i>quick-report</i> melalui integrasi Kamera & QR Code), transparansi progres penanganan secara real-time melalui <i>Vertical Stepper Timeline</i>, serta otomasi kecerdasan buatan berbasis Google Gemini 2.5 Flash untuk analisis tren kerusakan dan <i>Composite Urgency Scoring Engine</i>.
    """
    summary_table = Table([[Paragraph(summary_html, callout_style)]], colWidths=[515])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(summary_table)

    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # FUNGSI HELPER MENAMPILKAN MOCKUP + PENJELASAN (DUA KOLOM)
    # --------------------------------------------------------------------------
    def render_module_section(mod_code, mod_title, mockup_path, tujuan, komponen_list, logika_list, ux_notes):
        story.append(Paragraph(f"<b>{mod_code}: {mod_title}</b>", h1_style))
        story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#94A3B8"), spaceBefore=2, spaceAfter=12))

        # Komponen Kiri: Gambar Mockup (Width ~ 190 pt, Height ~ 380 pt)
        img_flowable = RLImage(mockup_path, width=195, height=390)

        # Komponen Kanan: Penjelasan Teknis Berstruktur
        right_flowables = [
            Paragraph("<b>🎯 Tujuan Antarmuka:</b>", h2_style),
            Paragraph(tujuan, body_style),
            Spacer(1, 4),
            Paragraph("<b>🧩 Komponen & Elemen Kunci:</b>", h2_style),
        ]
        for comp in komponen_list:
            right_flowables.append(Paragraph(f"• {comp}", bullet_style))

        right_flowables.extend([
            Spacer(1, 4),
            Paragraph("<b>⚙️ Logika Bisnis & Validasi:</b>", h2_style),
        ])
        for log in logika_list:
            right_flowables.append(Paragraph(f"• {log}", bullet_style))

        right_flowables.extend([
            Spacer(1, 6),
            Table([[Paragraph(f"<b>Catatan UX / Interaksi:</b> {ux_notes}", callout_style)]], colWidths=[305], style=[
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                ('PADDING', (0,0), (-1,-1), 6),
            ])
        ])

        # Tabel Layout Dua Kolom: [Gambar Mockup (200pt) | Penjelasan (315pt)]
        layout_table = Table([[img_flowable, right_flowables]], colWidths=[200, 315])
        layout_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))

        story.append(layout_table)
        story.append(PageBreak())

    # --------------------------------------------------------------------------
    # HALAMAN 2: MODUL 1 (MOD-01) - AUTENTIKASI & REGISTRASI
    # --------------------------------------------------------------------------
    render_module_section(
        mod_code="MODUL 1 (MOD-01)",
        mod_title="Autentikasi, Registrasi & Hak Akses Pengguna",
        mockup_path=m1,
        tujuan="Menyediakan gerbang akses yang aman dan membedakan hak akses secara otomatis antara Mahasiswa (pelapor fasilitas) dan Administrator (evaluator & penangan fasilitas) melalui JWT Token.",
        komponen_list=[
            "<b>Header & Logo Identitas:</b> Memperkuat branding fasilitas resmi kampus.",
            "<b>Role Toggle Pill:</b> Mempermudah pengguna beralih antara portal Mahasiswa dan Administrator.",
            "<b>Input NIM & Password:</b> Input teks tervalidasi dengan ikon visibilitas kata sandi (show/hide password).",
            "<b>Tombol Masuk Utama:</b> Tombol aksi kontras tinggi (Navy Blue) dengan status loading saat autentikasi.",
            "<b>Single Sign-On (SSO):</b> Opsi integrasi login akun kampus.",
            "<b>Registrasi Akun Baru:</b> Tautan menuju form pendaftaran akun baru."
        ],
        logika_list=[
            "Validasi format NIM numerik minimal 8 digit dan password minimal 6 karakter.",
            "Hashing kata sandi menggunakan pustaka bcrypt pada backend FastAPI.",
            "Penerbitan token JSON Web Token (JWT) yang disimpan di Flutter Secure Storage.",
            "Pencegahan brute-force dengan feedback error visual instan jika kredensial salah."
        ],
        ux_notes="Form otomatis mendeteksi tombol Enter pada keyboard untuk trigger submit, dan field input memiliki auto-focus untuk kecepatan pengguna."
    )

    # --------------------------------------------------------------------------
    # HALAMAN 3: MODUL 2 (MOD-02) - FORMULIR PELAPORAN & MEDIA/QR
    # --------------------------------------------------------------------------
    render_module_section(
        mod_code="MODUL 2 (MOD-02)",
        mod_title="Pelaporan Kerusakan Fasilitas & Integrasi Kamera/QR",
        mockup_path=m2,
        tujuan="Memfasilitasi pelaporan fasilitas rusak secara instan di lapangan melalui bukti visual foto kamera smartphone atau pemindaian QR Code fasilitas di lokasi kejadian.",
        komponen_list=[
            "<b>Segmented Input Tab:</b> Pilihan fleksibel antara 'Ambil Foto Fisik' atau 'Scan QR Code Fasilitas'.",
            "<b>Interactive Photo Frame:</b> Area preview foto kerusakan yang diambil langsung via kamera ponsel atau galeri foto.",
            "<b>Kategori Kerusakan (Filter Chips):</b> Tombol pill sekali-klik: Kursi, Proyektor, AC/Lampu, dan DLL.",
            "<b>Dropdown Lokasi Terstruktur:</b> Hirarki pemilihan Gedung, Lantai, dan Nomor Ruangan.",
            "<b>Field Deskripsi Kerusakan:</b> Input multiline untuk catatan spesifik kondisi kerusakan.",
            "<b>Selector Urgensi:</b> Opsi tingkat keparahan (Rendah, Sedang, Tinggi) dengan indikator warna."
        ],
        logika_list=[
            "Validasi wajib foto sebelum form dapat dikirim ke server.",
            "Pemindaian QR Code langsung mem-parsing ID Fasilitas dan mengunci lokasi tanpa perlu input manual.",
            "Upload file gambar diproses secara multipart/form-data dan disimpan aman di server backend.",
            "Pembuatan nomor tiket unik otomatis (#TK-xxxx) setelah sukses tersimpan."
        ],
        ux_notes="Di aplikasi Android native tombol kamera langsung mengaktifkan kamera ponsel tanpa dialog file picker, menghasilkan pengalaman pemotretan cepat."
    )

    # --------------------------------------------------------------------------
    # HALAMAN 4: MODUL 3 (MOD-03) - PELACAKAN STATUS & TIMELINE VERTIKAL
    # --------------------------------------------------------------------------
    render_module_section(
        mod_code="MODUL 3 (MOD-03)",
        mod_title="Pelacakan Status Tiket & Vertical Timeline",
        mockup_path=m3,
        tujuan="Memberikan transparansi penuh kepada mahasiswa pelapor mengenai tahapan penanganan fasilitas oleh teknisi kampus melalui visualisasi timeline vertikal (stepper).",
        komponen_list=[
            "<b>Header Tiket Interaktif:</b> Menampilkan Nomor Tiket (#TK-0058), Badge Status terkini, dan judul fasilitas.",
            "<b>Kartu Metadata Fasilitas:</b> Informasi detail lokasi (Gedung A, Ruang 301) dan stempel waktu pengajuan.",
            "<b>Vertical Stepper Timeline:</b> 4 tahapan penanganan terstruktur (Diajukan -> Disposisi -> Penanganan Teknisi -> Selesai).",
            "<b>Indikator Node Berwarna:</b> Warna hijau untuk tahap yang telah tuntas, biru berdenyut untuk tahap aktif, dan abu-abu untuk tahap berikutnya.",
            "<b>Catatan Log Teknisi:</b> Keterangan aksi nyata teknisi di lapangan (misal: 'Sedang mengganti baut sandaran').",
            "<b>Tombol Tanya Admin:</b> Membuka jalur klarifikasi langsung jika penanganan terhambat."
        ],
        logika_list=[
            "State status tiket di-query realtime dari endpoint `GET /api/v1/reports/{id_laporan}`.",
            "Setiap pembaruan status oleh admin/teknisi otomatis menambahkan node riwayat ke database.",
            "Penyaringan tab di daftar utama: Semua, Diajukan, Diproses, Selesai, dan Ditolak.",
            "Penyusunan data descending (laporan terbaru tampil di posisi teratas)."
        ],
        ux_notes="Pengguna dapat melakukan 'Pull-to-Refresh' untuk memperbarui progres penanganan tanpa harus kembali ke menu utama."
    )

    # --------------------------------------------------------------------------
    # HALAMAN 5: MODUL 4 (MOD-04) - DASHBOARD ADMIN & DISPOSISI
    # --------------------------------------------------------------------------
    render_module_section(
        mod_code="MODUL 4 (MOD-04)",
        mod_title="Dashboard Eksekutif Admin & Manajemen Disposisi",
        mockup_path=m4,
        tujuan="Menyediakan pusat kendali bagi pengelola sarana kampus untuk memantau volume kerusakan, mengevaluasi tiket masuk, menjadwalkan teknisi, atau menolak laporan tidak valid.",
        komponen_list=[
            "<b>Kartu Metrik KPI Klik-able:</b> 3 kartu ringkasan cepat: 'Diproses' (6), 'Selesai' (7), dan 'Total' (48). Mengklik kartu langsung menyaring daftar tiket.",
            "<b>Grafik Batang Kategori:</b> Distribusi kerusakan (Kursi 77%, Proyektor 23%) untuk monitoring rasio aset bermasalah.",
            "<b>Panel Evaluasi Tiket Cepat:</b> Menampilkan data tiket yang memerlukan persetujuan segera.",
            "<b>Tombol Aksi Terima vs Tolak:</b> 'Terima & Jadwalkan' (hijau) atau 'Tolak Laporan' (merah outline).",
            "<b>Dialog Input Alasan & Teknisi:</b> Modal penugasan nama teknisi dan alasan penolakan.",
            "<b>Bottom Navigation Shell:</b> Navigasi cepat antara Dashboard, Kelola Laporan, AI Rangkuman, dan Prioritas."
        ],
        logika_list=[
            "Perubahan status memicu pencatatan entitas audit trail `TINDAKAN_PENANGANAN` di database backend.",
            "Penolakan tiket mewajibkan input alasan penolakan minimal 5 karakter.",
            "Pembaruan status secara otomatis memperbarui count badge KPI dashboard.",
            "Dukungan filter multi-kategori dan pencarian teks nama ruangan."
        ],
        ux_notes="Kartu metrik atas dirancang responsif dengan gesture 'InkWell' yang memberikan feedback sentuhan haptik saat ditekan."
    )

    # --------------------------------------------------------------------------
    # HALAMAN 6: MODUL 5 (MOD-05) - ANALISIS & RANGKUMAN EKSEKUTIF AI
    # --------------------------------------------------------------------------
    render_module_section(
        mod_code="MODUL 5 (MOD-05)",
        mod_title="Rangkuman Eksekutif & Analisis Tren Berbasis AI",
        mockup_path=m5,
        tujuan="Meringkas ratusan komplain fasilitas secara otomatis menggunakan LLM (Google Gemini 2.5 Flash) agar pimpinan kampus dapat mengambil keputusan perbaikan yang tepat sasaran.",
        komponen_list=[
            "<b>Filter Periode & Lokasi Gedung:</b> Menyaring cakupan data sebelum dianalisis oleh engine AI.",
            "<b>Kartu AI Bergradien Ungu:</b> Desain premium yang menandakan output kecerdasan buatan Gemini AI.",
            "<b>Tiga Poin Eksekutif Utama:</b> Sintesis data otomatis (identifikasi aset paling sering rusak, area hotspot, dan volume antrean kritis).",
            "<b>Kotak Rekomendasi Kebijakan (Amber Card):</b> Saran strategis manajemen sarana kampus (misal: pengadaan spare-part massal).",
            "<b>Statistik Penunjang:</b> Persentase kerusakan (77% Kursi) dan titik rawan (Gedung A).",
            "<b>Tombol Ekspor Dokumen:</b> Kemudahan mendownload ringkasan ke format Word (.docx) atau PDF."
        ],
        logika_list=[
            "Backend mengagregasi data JSON laporan menjadi prompt terstruktur untuk Gemini API.",
            "Jika kuota API habis, sistem otomatis beralih (*graceful fallback*) ke modul Heuristic NLP bawaan.",
            "Hasil analisis dicatat ke entitas `ANALISIS_AI` dengan stempel waktu dan filter yang digunakan.",
            "Penanganan error asinkron sehingga UI tidak mengalami freezing saat kalkulasi AI berjalan."
        ],
        ux_notes="Terdapat animasi shimmer/skeleton loading saat AI sedang menganalisis data, memberikan kejelasan bahwa sistem sedang memproses kalkulasi cerdas."
    )

    # --------------------------------------------------------------------------
    # HALAMAN 7: MODUL 6 (MOD-06) - ENGINE PRIORITASI & SCORING AI
    # --------------------------------------------------------------------------
    render_module_section(
        mod_code="MODUL 6 (MOD-06)",
        mod_title="Engine Prioritasi Tiket & Scoring Penanganan AI",
        mockup_path=m6,
        tujuan="Menentukan urutan antrean penanganan tiket teknisi secara objektif berdasarkan skor urgensi matematis komposit (0 - 100), memastikan fasilitas paling krusial ditangani pertama kali.",
        komponen_list=[
            "<b>Banner Formula Scoring:</b> Transparansi rumus komposit: <i>Skor = 40% Keparahan + 30% Frekuensi + 30% Dampak</i>.",
            "<b>Daftar Kartu Tiket Berperingkat:</b> Kartu tiket tersusun dari Rank 1 hingga N sesuai urgensi tertinggi.",
            "<b>Badge Skor Numerik & Warna Urgensi:</b> Merah (Tinggi: 80-100), Kuning (Sedang: 50-79), Hijau (Rendah: <50).",
            "<b>Rincian Komponen Nilai:</b> Breakdown nilai ketiga parameter (Keparahan x/40, Frekuensi y/30, Dampak z/30).",
            "<b>Filter Tingkat Urgensi:</b> Menyaring daftar berdasarkan kategori Tinggi, Sedang, atau Rendah.",
            "<b>Tombol Disposisi Cepat:</b> Menjadwalkan tiket teratas ke tim teknisi siaga hanya dalam sekali tekan."
        ],
        logika_list=[
            "Kalkulasi komposit multi-kriteria: bobot keparahan (40%), riwayat frekuensi kerusakan aset serupa (30%), dan dampak lokasi (30%).",
            "Endpoint backend: `POST /api/v1/ai/prioritize-tickets` dan `GET /api/v1/ai/prioritized-tickets`.",
            "Penyusunan sorting tiket secara otomatis berdasarkan descending skor komposit.",
            "Tersedia modal penjelasan rinci perhitungan matematis untuk audit civitas akademika."
        ],
        ux_notes="Badge skor didesain mencolok di sudut kanan atas setiap kartu sehingga mata administrator langsung tertuju pada tiket darurat."
    )

    # --------------------------------------------------------------------------
    # HALAMAN 8: SISTEM DESAIN & PANDUAN WARNA (DESIGN SYSTEM GUIDE)
    # --------------------------------------------------------------------------
    story.append(Paragraph("<b>Panduan Sistem Desain & Arsitektur UI/UX</b>", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#94A3B8"), spaceBefore=2, spaceAfter=15))

    story.append(Paragraph("<b>1. Palet Warna Standar (Design System Palette)</b>", h2_style))
    story.append(Paragraph("Aplikasi menggunakan palet warna yang memenuhi standar aksesibilitas WCAG 2.1 AA dengan kontras tinggi:", body_style))

    color_data = [
        [Paragraph("<b>Role / Token</b>", body_style), Paragraph("<b>Nama Warna</b>", body_style), Paragraph("<b>Kode Hex</b>", body_style), Paragraph("<b>Penggunaan Utama</b>", body_style)],
        [Paragraph("Primary Brand", body_style), Paragraph("Deep Navy Blue", body_style), Paragraph("<code>#1E3A8A</code>", body_style), Paragraph("App bar, tombol utama, teks judul, header cover", body_style)],
        [Paragraph("Secondary Brand", body_style), Paragraph("Vibrant Blue", body_style), Paragraph("<code>#2563EB</code>", body_style), Paragraph("Sub-heading, link aktif, progress bar aktif", body_style)],
        [Paragraph("Status: Diajukan", body_style), Paragraph("Amber Gold", body_style), Paragraph("<code>#D97706</code>", body_style), Paragraph("Badge laporan baru masuk, prioritas Sedang", body_style)],
        [Paragraph("Status: Diproses", body_style), Paragraph("Cobalt Blue", body_style), Paragraph("<code>#1D4ED8</code>", body_style), Paragraph("Badge laporan sedang dikerjakan teknisi", body_style)],
        [Paragraph("Status: Selesai", body_style), Paragraph("Emerald Green", body_style), Paragraph("<code>#16A34A</code>", body_style), Paragraph("Badge tiket tuntas, verifikasi valid, success toast", body_style)],
        [Paragraph("Status: Ditolak", body_style), Paragraph("Crimson Red", body_style), Paragraph("<code>#DC2626</code>", body_style), Paragraph("Badge tiket ditolak, alert prioritas Tinggi / bahaya", body_style)],
        [Paragraph("AI Accent", body_style), Paragraph("Royal Purple", body_style), Paragraph("<code>#7C3AED</code>", body_style), Paragraph("Badge Gemini AI, rangkuman eksekutif cerdas", body_style)],
        [Paragraph("Surface / Base", body_style), Paragraph("Light Slate", body_style), Paragraph("<code>#F8FAFC</code>", body_style), Paragraph("Background aplikasi, card surface, input border", body_style)],
    ]
    color_table = Table(color_data, colWidths=[95, 95, 80, 245])
    color_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(color_table)

    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>2. Standar Tipografi & Geometri Komponen</b>", h2_style))
    
    specs = [
        "<b>Tipografi:</b> Menggunakan font sans-serif modern (Segoe UI / Roboto / Inter) dengan skala hierarki yang tegas (Heading: 20-24pt Bold, Subhead: 13-15pt SemiBold, Body: 10-12pt Regular, Caption: 8-9pt).",
        "<b>Sudut Lengkung (Border Radius):</b> Konsisten menggunakan radius 10px - 12px untuk kartu (Cards) dan tombol (Buttons), serta 6px - 8px untuk form input dan chip badges.",
        "<b>Elevasi & Bayangan (Elevation):</b> Kartu mengutamakan outline tipis border 1px (<code>#E2E8F0</code>) dipadukan dengan subtle shadow untuk performa rendering optimal di perangkat mobile spek menengah.",
        "<b>Target Sentuh (Touch Target Area):</b> Seluruh tombol, tab, dan chip interaktif memiliki tinggi minimal 44x44 dp sesuai panduan Material Design 3."
    ]
    for s in specs:
        story.append(Paragraph(f"• {s}", bullet_style))

    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>3. Alur Pengguna Terintegrasi (End-to-End User Journey)</b>", h2_style))

    journey_steps = [
        "<b>Tahap 1 (Pelaporan):</b> Mahasiswa login -> Membuka form -> Memotret kerusakan fisik / scan QR -> Form otomatis terisi -> Menekan tombol Kirim -> Mendapatkan Nomor Tiket.",
        "<b>Tahap 2 (Otomasi AI):</b> Server FastAPI memvalidasi data -> Engine Prioritasi MOD-06 menghitung skor komposit (0-100) -> Tiket terdaftar dalam daftar urutan teknisi.",
        "<b>Tahap 3 (Tindakan Admin):</b> Pengelola sarana melihat notifikasi di Dashboard MOD-04 -> Meninjau bukti foto -> Mengklik 'Terima & Jadwalkan' -> Status berpindah ke 'Diproses'.",
        "<b>Tahap 4 (Pelacakan & Penyelesaian):</b> Mahasiswa memantau pergerakan timeline vertikal MOD-03 -> Teknisi menyelesaikan pekerjaan di lokasi -> Status diperbarui ke 'Selesai'.",
        "<b>Tahap 5 (Rangkuman Eksekutif):</b> Data terakumulasi di MOD-05 -> Gemini AI merangkum tren kerusakan semesteran sebagai dasar penganggaran fasilitas kampus."
    ]
    for j in journey_steps:
        story.append(Paragraph(f"• {j}", bullet_style))

    # Build PDF
    print(f"Menyusun dokumen PDF ke {PDF_PATH}...")
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Selesai! PDF berhasil dibuat.")
    return PDF_PATH

if __name__ == "__main__":
    build_pdf_document()
