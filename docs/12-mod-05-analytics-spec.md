# Spesifikasi Teknis MOD-05: Subsistem Analytics & Rangkuman Eksekutif AI

## 📌 Ringkasan Modul
Modul ini mengimplementasikan ekstraksi pola kerusakan fasilitas kampus dan sintesis ringkasan eksekutif berbasis kecerdasan buatan (*Google Gemini API*) sesuai dengan **Diagram 5 Aktivitas UML** dan entitas database `ANALISIS_AI`.

---

## 🛠️ REST API Endpoints (FastAPI)

### 1. Filter & Aggregation AI Summarization Pipeline
- **Endpoint**: `POST /api/v1/analytics/summary`
- **Request Body**:
```json
{
  "periode": "Oktober 2026",
  "gedung": "Semua Gedung",
  "kategori": "Semua Kategori"
}
```
- **Response Sukses (Data Ditemukan)**:
```json
{
  "found": true,
  "id_analisis": "ANL-9577315D",
  "filter_label": "Oktober 2026 · Semua Gedung · Semua Kategori",
  "total_laporan": 34,
  "bullets": [
    "Kursi menjadi fasilitas paling sering rusak (12 laporan, 35%).",
    "Gedung A mencatat 14 laporan, mendominasi area fasilitas bermasalah.",
    "3 laporan berkeparahan tinggi masih berstatus Diajukan."
  ],
  "rekomendasi": "Jadwalkan perbaikan kursi massal dan inspeksi menyeluruh di Gedung A.",
  "statistik": {
    "top_kategori": "Kursi",
    "top_kategori_count": 12,
    "top_kategori_pct": 35,
    "top_gedung": "Gedung A",
    "top_gedung_count": 14,
    "tiket_kritis_menunggu": 3
  },
  "created_at": "2026-11-06T16:18:25Z"
}
```
- **Response Skenario Data Tidak Ditemukan**:
  - `found: false` beserta pesan panduan mengatur ulang filter pencarian (Slide 26 mockup).

### 2. Riwayat Analisis AI
- **Endpoint**: `GET /api/v1/analytics/history`
- **Response**: Menampilkan histori seluruh hasil sintesis ringkasan eksekutif yang pernah di-generate dan tersimpan di database `ANALISIS_AI`.

---

## 📱 Implementasi Frontend (Flutter)

1. **`AiSummaryScreen`** (`lib/screens/analytics/ai_summary_screen.dart`):
   - **Tampilan 1: Filter Setup** (Slide 24):
     - Pilihan Periode, Gedung, dan Kategori fasilitas.
     - Tombol **Generate Rangkuman AI** dengan ikon sparkle AI.
     - Chip simulasi: *"Uji skenario: data tidak ditemukan"*.
   - **Tampilan 2: Executive Summary Card** (Slide 25):
     - Chip ringkasan parameter filter (*Okt 2026 · Semua Gedung · Semua Kategori*).
     - Card visual **Rangkuman Eksekutif** berisi 3 butir ekstraksi pola AI (kerusakan dominan, tren gedung, status laporan kritis).
     - Highlight Box **Rekomendasi Strategis** untuk biro fasilitas kampus.
     - Tombol **Atur Ulang Filter**.
   - **Tampilan 3: Data Tidak Ditemukan** (Slide 26):
     - Ilustrasi ikon tanda tanya, pesan panduan (*"Tidak ada laporan yang sesuai dengan filter yang dipilih"*), dan tombol **Ubah Filter**.
2. **Navigasi Terintegrasi**:
   - Menu **Rangkum** pada `AdminNavigationShell` terhubung langsung ke `AiSummaryScreen`.
