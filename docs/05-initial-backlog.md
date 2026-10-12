# 05. Initial Product Backlog — Student Facility Reporting

Dokumen ini memuat daftar kebutuhan fitur awal dalam format **User Story**, disusun berdasarkan prioritas **MoSCoW** (*Must have, Should have, Could have, Won't have*), penanggung jawab utama, serta kriteria penerimaan (*Acceptance Criteria*).

---

## 📋 Tabel Ringkasan Backlog (US-01 s.d. US-12)

| ID | User Story | Prioritas | Pemilik Peran |
| :--- | :--- | :---: | :--- |
| **US-01** | Sebagai mahasiswa atau petugas, saya ingin login menggunakan akun terdaftar agar aktivitas dan riwayat laporan terikat pada identitas saya. | **Must** | Hacker (Fakhrulrijal) |
| **US-02** | Sebagai mahasiswa, saya ingin mengisi formulir laporan (lokasi gedung, ruangan, deskripsi) agar kerusakan fasilitas dapat tercatat dengan spesifik. | **Must** | Hipster (Muhammad) & Hacker |
| **US-03** | Sebagai mahasiswa, saya ingin mengambil atau mengunggah foto kerusakan fasilitas agar petugas dapat melihat bukti visual kondisi riil. | **Must** | Hacker (Fakhrulrijal) |
| **US-04** | Sebagai mahasiswa, saya ingin laporan saya tersimpan sebagai tiket dengan status awal agar dapat diproses oleh petugas. | **Must** | Hacker (Fakhrulrijal) |
| **US-05** | Sebagai mahasiswa, saya ingin melihat daftar tiket laporan milik saya beserta status penanganannya agar saya mengetahui perkembangannya. | **Must** | Hipster (Muhammad) |
| **US-06** | Sebagai petugas, saya ingin melihat daftar seluruh tiket laporan masuk beserta detail foto dan lokasinya agar dapat ditindaklanjuti. | **Must** | Hacker & Hipster |
| **US-07** | Sebagai mahasiswa, saya ingin melihat rekomendasi kategori dari AI berdasarkan foto yang diunggah dan dapat mengubahnya agar pelaporan lebih cepat dan akurat. | **Should** | Hustler (Roni) & Hacker |
| **US-08** | Sebagai petugas fasilitas, saya ingin memverifikasi atau mengoreksi kategori fasilitas pada tiket laporan agar data inventaris akhir tetap valid. | **Should** | Hacker (Fakhrulrijal) |
| **US-09** | Sebagai petugas fasilitas, saya ingin memfilter daftar tiket berdasarkan kategori, status, dan gedung agar penanganan lebih terorganisir. | **Should** | Hipster (Muhammad) |
| **US-10** | Sebagai petugas fasilitas, saya ingin memperbarui status tiket (Diproses / Selesai / Ditolak) disertai catatan penjelasan agar pelapor mendapatkan kejelasan. | **Should** | Hacker (Fakhrulrijal) |
| **US-11** | Sebagai pengguna, saya ingin logout dari aplikasi agar sesi akun saya di perangkat dapat dihentikan dengan aman. | **Should** | Hipster & Hacker |
| **US-12** | Sebagai mahasiswa, saya ingin melihat catatan riwayat pembaruan status pada detail tiket agar proses perbaikan transparan. | **Could** | Hipster (Muhammad) |

---

## 🔍 Detail Kriteria Penerimaan (*Acceptance Criteria*)

### 🔴 Must-Have (Fitur Inti MVP)

#### US-01: Autentikasi Pengguna (Login & Registrasi)
- **Sebagai**: Mahasiswa dan Petugas Fasilitas
- **Acceptance Criteria**:
  - [ ] Pengguna dapat memasukkan email dan kata sandi.
  - [ ] Sistem memvalidasi format email dan kecocokan sandi via Firebase Authentication.
  - [ ] Pengguna diarahkan ke dashboard sesuai dengan peran (*Role*: Mahasiswa / Petugas).
  - [ ] Pesan kesalahan muncul jika kredensial salah.

#### US-02: Formulir Pelaporan Fasilitas
- **Sebagai**: Mahasiswa
- **Acceptance Criteria**:
  - [ ] Pengguna dapat memilih Gedung dari dropdown yang disediakan.
  - [ ] Pengguna dapat menginput nama Ruangan/Lokasi secara spesifik.
  - [ ] Pengguna wajib mengisikan deskripsi singkat kerusakan minimal 10 karakter.
  - [ ] Validasi form mencegah pengiriman data kosong.

#### US-03: Unggah Foto Bukti Kerusakan
- **Sebagai**: Mahasiswa
- **Acceptance Criteria**:
  - [ ] Pengguna dapat memilih sumber foto: Kamera langsung atau Galeri perangkat.
  - [ ] Menampilkan pratinjau (*preview*) foto sebelum laporan dikirimkan.
  - [ ] Foto dikompresi sebelum diunggah ke Firebase Storage untuk efisiensi kuota.

#### US-04: Penyimpanan Tiket Laporan
- **Sebagai**: Mahasiswa
- **Acceptance Criteria**:
  - [ ] Ketika tombol *Kirim Laporan* ditekan, data tersimpan ke Cloud Firestore.
  - [ ] Tiket otomatis mendapatkan `id` unik, `timestamp` pembuatan, dan status `"baru"`.
  - [ ] Menampilkan pesan sukses pengiriman dan mengarahkan pengguna kembali ke daftar tiket.

#### US-05: Tampilan Riwayat Tiket Pelapor
- **Sebagai**: Mahasiswa
- **Acceptance Criteria**:
  - [ ] Menampilkan daftar tiket yang diajukan oleh pengguna yang sedang login.
  - [ ] Setiap item menampilkan thumbnail foto, lokasi, kategori, dan lencana (*badge*) status berwarna.
  - [ ] Pengguna dapat mengklik item untuk membuka tampilan detail tiket.

#### US-06: Tampilan Daftar Tiket Masuk untuk Petugas
- **Sebagai**: Petugas Fasilitas
- **Acceptance Criteria**:
  - [ ] Petugas dapat melihat seluruh tiket dari semua mahasiswa secara kronologis (terbaru di atas).
  - [ ] Menampilkan indikator status tiket yang belum diverifikasi.
  - [ ] Petugas dapat membuka halaman detail tiket untuk memeriksa foto dan deskripsi laporan.

---

### 🟡 Should-Have (Fitur Pendukung Penting)

#### US-07: Saran Kategori AI Vision
- **Sebagai**: Mahasiswa
- **Acceptance Criteria**:
  - [ ] Setelah foto dipilih, sistem mengirim foto ke Google Gemini Vision API.
  - [ ] Sistem menampilkan kartu saran: nama kategori yang terdeteksi, kondisi, dan persentase keyakinan.
  - [ ] Mahasiswa dapat menekan tombol *Gunakan Saran Ini* atau memilih opsi *Ubah Kategori Secara Manual*.
  - [ ] Jika analisis AI gagal/timeout, sistem tetap mengizinkan pemilihan manual tanpa kendala.

#### US-08: Verifikasi & Koreksi Kategori oleh Petugas
- **Sebagai**: Petugas Fasilitas
- **Acceptance Criteria**:
  - [ ] Pada detail tiket, petugas memiliki opsi untuk mengonfirmasi atau memilih kategori lain dari dropdown.
  - [ ] Perubahan kategori tercatat pada riwayat audit tiket.

#### US-09: Filter & Pencarian Tiket
- **Sebagai**: Petugas Fasilitas
- **Acceptance Criteria**:
  - [ ] Petugas dapat memfilter daftar berdasarkan status (`baru`, `diproses`, `selesai`).
  - [ ] Petugas dapat memfilter berdasarkan kategori fasilitas (misal: *AC*, *Kursi*).

#### US-10: Pembaruan Status & Catatan Penanganan
- **Sebagai**: Petugas Fasilitas
- **Acceptance Criteria**:
  - [ ] Petugas dapat mengubah status tiket menjadi: `diverifikasi`, `diproses`, `selesai`, atau `ditolak`.
  - [ ] Wajib mengisi kolom catatan/tindak lanjut (misal: *"Teknisi dijadwalkan Rabu pk 10.00"*).
  - [ ] Status log baru ditambahkan ke koleksi `StatusLog`.

#### US-11: Logout Pengguna
- **Sebagai**: Mahasiswa dan Petugas
- **Acceptance Criteria**:
  - [ ] Tombol logout tersedia di menu profil/pengaturan.
  - [ ] Sesi lokal dihapus dan pengguna diarahkan ke layar login.

---

### 🟢 Could-Have (Fitur Tambahan)

#### US-12: Riwayat Log Status Transparan
- **Sebagai**: Mahasiswa
- **Acceptance Criteria**:
  - [ ] Pada detail tiket, mahasiswa dapat melihat linimasa (*timeline*) perubahan status tiket beserta catatan yang diberikan oleh petugas fasilitas.
