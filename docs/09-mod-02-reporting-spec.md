# Spesifikasi Teknis MOD-02: Pelaporan Kerusakan & QR Scanner

## 📌 Ringkasan Modul
Modul ini mengimplementasikan alur pelaporan fasilitas kampus yang rusak sesuai dengan **Diagram 2 Aktivitas UML** dan entitas database `LAPORAN`, `FASILITAS`, serta `STATUS_TIKET`.

---

## 🛠️ REST API Endpoints (FastAPI)

### 1. Pembacaan QR Code Aset Fasilitas
- **Endpoint**: `GET /api/v1/fasilitas/qr/{kode_qr}`
- **Contoh Request**: `GET /api/v1/fasilitas/qr/KR-A002-07`
- **Response Sukses (200 OK)**:
```json
{
  "id_fasilitas": "FAS-001",
  "kode_qr": "KR-A002-07",
  "nama_fasilitas": "Kursi Kuliah Ergonomis",
  "lokasi_gedung": "Ruang A002 – Gedung A",
  "kategori": "Kursi",
  "kondisi_terakhir": "Normal"
}
```
- **Response Tidak Dikenali (404 Not Found)**:
```json
{
  "detail": "Kode QR 'UNKNOWN' tidak dikenali. Kode bukan milik fasilitas kampus atau rusak."
}
```

### 2. Pengajuan Laporan Fasilitas Baru
- **Endpoint**: `POST /api/v1/laporan` (Multipart Form-Data)
- **Field**:
  - `foto`: File gambar (JPEG/PNG)
  - `lokasi`: Lokasi ruangan & gedung fasilitas
  - `kategori`: Kursi, Meja, Proyektor, AC, Lampu, Lainnya
  - `tingkat_keparahan`: Ringan, Sedang, Berat
  - `deskripsi`: Penjelasan detail kerusakan
  - `kode_qr`: Opsional (kode aset hasil scan)
- **Response**: `201 Created`
  - Menerbitkan Nomor Tiket otomatis (misal: `#TK-0012`).
  - Status tiket otomatis: `"Diajukan"`.
  - Mengunggah foto ke folder penyimpanan media (`/uploads/`).
  - Mencatat histori status tiket awal pada entitas `STATUS_TIKET`.

---

## 📱 Implementasi Frontend (Flutter)
1. **`CreateReportScreen`** (`lib/screens/report/create_report_screen.dart`):
   - Tab navigasi `Foto` & `Scan QR`.
   - Panduan pengambilan foto (cahaya cukup, objek jelas dalam frame).
2. **`QrScannerScreen`** (`lib/screens/report/qr_scanner_screen.dart`):
   - Viewfinder pemindaian QR Code aset fasilitas.
   - Dialog "QR Terbaca" dengan auto-fill lokasi dan kategori ke formulir laporan.
   - Skenario fallback "QR Tidak Dikenali" dengan tombol "Isi Lokasi Manual".
3. **`ReportFormScreen`** (`lib/screens/report/report_form_screen.dart`):
   - Formulir input data fasilitas, kategori chips, tingkat keparahan, deskripsi kerusakan.
4. **`ReviewReportScreen`** (`lib/screens/report/review_report_screen.dart`):
   - Pratinjau ringkasan sebelum pengiriman tiket ke server.
5. **`ReportSuccessScreen`** (`lib/screens/report/report_success_screen.dart`):
   - Tampilan konfirmasi penerbitan tiket `#TK-0012` dengan status "Diajukan".
