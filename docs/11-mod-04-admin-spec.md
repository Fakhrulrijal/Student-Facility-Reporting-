# Spesifikasi Teknis MOD-04: Dashboard Admin & Kelola Tiket Perbaikan

## 📌 Ringkasan Modul
Modul ini mengimplementasikan pusat kendali admin dan verifikasi kelayakan tiket kerusakan fasilitas kampus sesuai dengan **Diagram 4 Aktivitas UML** dan entitas database `LAPORAN`, `STATUS_TIKET`, serta `TINDAKAN_PENANGANAN`.

---

## 🛠️ REST API Endpoints (FastAPI)

### 1. Ringkasan Statistik Dashboard Admin
- **Endpoint**: `GET /api/v1/admin/dashboard/summary`
- **Response (200 OK)**:
```json
{
  "total_laporan": 34,
  "menunggu_peninjauan": 5,
  "diproses": 8,
  "selesai": 21,
  "ditolak": 0,
  "breakdown_kategori": {
    "Kursi": 12,
    "Proyektor": 7,
    "Lampu / AC": 6,
    "DLL": 9
  }
}
```

### 2. Manajemen Seluruh Laporan
- **Endpoint**: `GET /api/v1/admin/laporan?status_filter={filter}`
- **Parameter Filter**: `Semua`, `Diajukan`, `Diproses`, `Selesai`, `Ditolak`
- **Response**: Menampilkan `total_laporan`, `menunggu_peninjauan`, dan list tiket lengkap beserta identitas pelapor dan NIM.

### 3. Workflow Verifikasi & Pembaruan Status Admin
- **Endpoint**: `PUT /api/v1/admin/laporan/{id_laporan}/status`
- **Request Body (Skenario Terima - Layak Diproses)**:
```json
{
  "status": "Diproses",
  "aksi_teknis": "Perbaiki",
  "catatan": "Sandaran akan diperbaiki teknisi pada hari Senin.",
  "admin_id": "USR-002",
  "admin_name": "Administrator Fasilitas"
}
```
- **Request Body (Skenario Tolak - Tidak Layak)**:
```json
{
  "status": "Ditolak",
  "alasan_penolakan": "Laporan duplikat — kerusakan yang sama sudah dilaporkan pada tiket #TK-0009.",
  "admin_id": "USR-002",
  "admin_name": "Administrator Fasilitas"
}
```
- **Response**: Mengembalikan status baru, entri `TINDAKAN_PENANGANAN`, dan resi pengiriman simulasi **Firebase Cloud Messaging (FCM)** ke perangkat pelapor.

---

## 📱 Implementasi Frontend (Flutter)

1. **`AdminDashboardScreen`** (`lib/screens/admin/admin_dashboard_screen.dart`):
   - Widget metrik 3 kartu ringkas (*8 Diproses*, *21 Selesai*, *34 Total*) sesuai Slide 18 mockup.
   - Breakdown statistik kerusakan per kategori (*Kursi*, *Proyektor*, *Lampu / AC*, *DLL*).
   - Akses cepat kartu *Kelola Laporan*, *Rangkuman AI*, dan *Prioritas Penanganan*.
2. **`AdminManageReportsScreen`** (`lib/screens/admin/admin_manage_reports_screen.dart`):
   - Segmented tab bar: *Semua*, *Diajukan*, *Diproses*, *Selesai*.
   - Banner subheader counter (*"34 laporan · 5 menunggu peninjauan"*) sesuai Slide 19 mockup.
   - List tiket dengan foto thumbnail, nama pelapor, tanggal, dan badge status.
3. **`AdminReportDetailScreen`** (`lib/screens/admin/admin_report_detail_screen.dart`):
   - Foto bukti kerusakan, detail kategori, gedung, keparahan, dan deskripsi pelapor.
   - Pertanyaan evaluasi: *"Laporan layak diproses?"* dengan tombol **Tolak** dan **Terima** (Slide 20 mockup).
4. **`AdminActionPlanScreen`** (`lib/screens/admin/admin_action_plan_screen.dart`):
   - Form penentuan tindakan teknis: pilihan **Perbaiki** vs **Ganti Baru**, dropdown status tiket (*Diproses* / *Selesai*), dan catatan teknisi (Slide 21 mockup).
5. **`AdminRejectReportScreen`** (`lib/screens/admin/admin_reject_report_screen.dart`):
   - Form penolakan tiket dengan validasi wajib mengisi alasan penolakan dan banner pemberitahuan notifikasi ke pelapor (Slide 22 mockup).
6. **`AdminStatusUpdatedScreen`** (`lib/screens/admin/admin_status_updated_screen.dart`):
   - Layar konfirmasi keberhasilan update status (contoh: *Tiket #TK-0012 → Diproses*) dengan pratinjau pesan push notification FCM (Slide 23 mockup).
7. **`AdminNavigationShell`** (`lib/screens/admin/admin_navigation_shell.dart`):
   - Navigasi bawah 4 menu: *Dashboard* | *Laporan* | *Rangkum* | *Prioritas*.
