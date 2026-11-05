# Spesifikasi Teknis MOD-03: Tracking Status & Histori Laporan Pelapor

## 📌 Ringkasan Modul
Modul ini mengimplementasikan pemantauan dan penelusuran status tiket laporan fasilitas secara real-time oleh mahasiswa/dosen pelapor sesuai dengan **Diagram 3 Aktivitas UML** dan relasi database `LAPORAN` dengan `STATUS_TIKET`.

---

## 🛠️ REST API Endpoints (FastAPI)

### 1. Daftar Laporan Pengguna Terfilter
- **Endpoint**: `GET /api/v1/laporan/user/{id_user}?status_filter={filter}`
- **Parameter**:
  - `id_user`: ID Pengguna (contoh: `USR-001`) atau NIM/NIP (contoh: `12345678`)
  - `status_filter` (Opsional): `Semua`, `Diproses`, `Selesai`, `Diajukan`
- **Response**: Array daftar tiket yang diajukan oleh pengguna terkait dengan informasi ringkas, tanggal, foto bukti, dan status terkini.

### 2. Riwayat Timeline Status Tiket
- **Endpoint**: `GET /api/v1/laporan/{id_laporan}/history`
- **Parameter**: `id_laporan` atau nomor tiket (contoh: `LAP-A07323B8` atau `TK-0012`)
- **Response**:
```json
{
  "id_laporan": "LAP-A07323B8",
  "nomor_tiket": "#TK-0012",
  "status_saat_ini": "Diproses",
  "timeline": [
    {
      "stage_key": "diajukan",
      "stage_name": "Diajukan",
      "is_completed": true,
      "is_current": false,
      "timestamp": "2026-10-29T10:15:00Z",
      "catatan": "Laporan berhasil diajukan ke sistem fasilitas kampus.",
      "petugas": "USR-001"
    },
    {
      "stage_key": "ditinjau_admin",
      "stage_name": "Ditinjau Admin",
      "is_completed": true,
      "is_current": false,
      "timestamp": "2026-10-29T11:00:00Z",
      "catatan": "Laporan diverifikasi layak perbaikan.",
      "petugas": "Admin Fasilitas"
    },
    {
      "stage_key": "diproses",
      "stage_name": "Diproses",
      "is_completed": true,
      "is_current": true,
      "timestamp": "2026-10-29T14:30:00Z",
      "catatan": "Sandaran akan diperbaiki teknisi pada hari Senin.",
      "petugas": "Teknisi Budi"
    },
    {
      "stage_key": "selesai",
      "stage_name": "Selesai",
      "is_completed": false,
      "is_current": false,
      "timestamp": null,
      "catatan": "–",
      "petugas": null
    }
  ],
  "logs": [...]
}
```

### 3. Pembaruan Status Tiket & Catatan Petugas
- **Endpoint**: `PUT /api/v1/laporan/{id_laporan}/status`
- **Request Body**:
```json
{
  "status": "Diproses",
  "catatan": "Sandaran akan diperbaiki teknisi pada hari Senin.",
  "updated_by": "Teknisi Budi"
}
```

---

## 📱 Implementasi Frontend (Flutter)

1. **`MyReportsScreen`** (`lib/screens/tracking/my_reports_screen.dart`):
   - **Segmented Tab Bar**: Filter instan 3 status: *Semua*, *Diproses*, *Selesai*.
   - **Ticket Card List**: Menampilkan thumbnail foto, kategori & ruangan (contoh: *Kursi - Ruang A002*), tanggal laporan, dan badge status berwarna (*Diajukan* / *Diproses* / *Selesai*).
   - **Empty State UI**: Menampilkan ilustrasi ikon tanda tanya, pesan panduan (*"Belum Ada Laporan: Laporan yang kamu buat akan tampil di sini"*), dan tombol *Buat Laporan* sesuai Slide 15 mockup.
2. **`ReportDetailScreen`** (`lib/screens/tracking/report_detail_screen.dart`):
   - Header tiket dan foto banner bukti kerusakan.
   - Ringkasan tingkat keparahan dan QR Code aset.
   - **`VerticalTimelineWidget`**: Komponen visual timeline vertikal 4 tahap (*Diajukan* -> *Ditinjau Admin* -> *Diproses* -> *Selesai*) lengkap dengan node bulat terkoneksi garis vertikal, timestamp real-time, dan kartu catatan teknisi perbaikan (Slide 16 mockup).
   - Fitur **Pull-to-Refresh** untuk sinkronisasi pembaruan status terkini.
3. **`MainNavigationShell`** (`lib/screens/home/main_navigation_shell.dart`):
   - Navigasi bawah terpadu (*Home* | *Laporan* | *Profil*) sesuai seluruh alur mockup Slide 6, 14, 15, dan 17.
