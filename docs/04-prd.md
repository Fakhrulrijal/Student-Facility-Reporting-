# 04. Product Requirements Document (PRD) — Student Facility Reporting

**Versi**: v1.0 (Pertemuan 1)  
**Status**: Disepakati Tim  
**Tim**: Fakhrulrijal (Hacker), Muhammad (Hipster), Roni (Hustler)  

---

## 1. Ringkasan Eksekutif
Aplikasi mobile **Student Facility Reporting** dirancang untuk menyelesaikan hambatan kategorisasi dalam pelaporan kerusakan sarana dan prasarana kampus. Aplikasi menyediakan antarmuka pelaporan cepat dengan pengambilan foto dan pemilihan lokasi, serta mengintegrasikan **Google Gemini Vision API** untuk menghasilkan draft rekomendasi kategori kerusakan yang seragam. Seluruh keputusan klasifikasi akhir tetap diverifikasi oleh pengguna atau petugas fasilitas.

---

## 2. Persona Pengguna

### Persona 1: Mahasiswa Pelapor (*Primary User*)
- **Profil**: Mahasiswa aktif yang sering menjumpai fasilitas rusak (kursi goyang/patah, proyektor mati, AC bocor) di ruang kuliah.
- **Kebutuhan**: Ingin melapor secara cepat lewat ponsel tanpa proses birokrasi berbelit dan tanpa kebingungan memilih nama kategori teknis.
- **Tujuan**: Memastikan laporannya diterima oleh pihak pengelola dan dapat dipantau progres perbaikannya.

### Persona 2: Petugas Fasilitas (*Internal Campus Operator*)
- **Profil**: Staf teknis pengelola sarana prasarana kampus yang bertugas memilah tiket dan menjadwalkan teknisi.
- **Kebutuhan**: Menerima laporan yang memiliki bukti foto jelas, lokasi spesifik, dan kategori kerusakan yang terstandarisasi.
- **Tujuan**: Memverifikasi validitas laporan, menentukan urgensi penanganan, dan mencatat status penyelesaian perbaikan.

---

## 3. Ruang Lingkup Produk (*Product Scope*)

### Dalam Cakupan (*In-Scope MVP*)
1. **Autentikasi Pengguna**: Login dan logout untuk peran Mahasiswa dan Petugas menggunakan Firebase Authentication.
2. **Formulir Laporan Kerusakan**: Form berisi data lokasi (gedung & ruangan), deskripsi teks masalah, dan kategori.
3. **Unggah Foto Kerusakan**: Pengambilan gambar dari kamera atau galeri dengan kompresi dan pratinjau.
4. **Rekomendasi AI Vision**: Analisis foto kerusakan menghasilkan saran kategori dan tingkat keyakinan (*confidence level*).
5. **Konfirmasi & Koreksi Kategori**: Mahasiswa dapat menerima atau mengganti saran kategori secara mandiri.
6. **Penyimpanan Tiket**: Tiket laporan tersimpan di Cloud Firestore dengan status default `"baru"`.
7. **Daftar & Detail Tiket**:
   - Mahasiswa: melihat riwayat tiket yang dilaporkan beserta status penanganannya.
   - Petugas: melihat daftar seluruh tiket masuk, memverifikasi kategori, dan mengubah status penanganan.

### Di Luar Cakupan (*Out-of-Scope MVP*)
- Sistem notifikasi push real-time yang kompleks.
- Integrasi Single Sign-On (SSO) LDAP universitas penuh (direncanakan untuk rilis pasca-MVP).
- Penentuan tingkat urgensi otomatis yang mengikat secara hukum.
- Algoritma pembersihan tiket duplikat secara otomatis.
- Dashboard visual analitik performa teknisi tingkat lanjut.

---

## 4. Kebutuhan Fungsional (*Functional Requirements*)

| Kode | Deskripsi Kebutuhan | User Story Terkait |
| :--- | :--- | :--- |
| **FR-01** | Sistem mendukung registrasi/login dan logout berbasis email & password untuk peran mahasiswa dan petugas. | US-01, US-11 |
| **FR-02** | Pengguna dapat menginput data laporan kerusakan berupa gedung, ruangan/lokasi spesifik, dan deskripsi kejadian. | US-02 |
| **FR-03** | Pengguna dapat mengambil foto dari kamera atau memilih dari galeri serta melihat pratinjau gambar. | US-03 |
| **FR-04** | Sistem menyimpan setiap laporan baru ke database dengan atribut status awal `"baru"`. | US-04 |
| **FR-05** | Mahasiswa dapat melihat daftar tiket laporan miliknya, detail foto, lokasi, kategori, dan status terkini. | US-05, US-12 |
| **FR-06** | Petugas fasilitas dapat melihat seluruh daftar tiket laporan masuk beserta filter sederhana. | US-06 |
| **FR-07** | Sistem mengirimkan foto ke API AI Vision dan menampilkan saran kategori fasilitas beserta alasan singkat. | US-07 |
| **FR-08** | Petugas dapat memverifikasi atau mengoreksi kategori akhir serta mengubah status tiket (Diproses / Selesai / Ditolak) dengan catatan. | US-08, US-10 |
| **FR-09** | Petugas dapat melakukan penyaringan (*filtering*) tiket berdasarkan kategori, status tiket, dan gedung. | US-09 |

---

## 5. Kebutuhan Non-Fungsional (*Non-Functional Requirements*)

- **Keamanan**: Data sensitif diamankan melalui Firebase Security Rules; kredensial pengguna di-hash oleh Firebase Auth.
- **Privasi Pengguna**: Foto laporan dibatasi hanya untuk verifikasi kerusakan fisik kampus. Aplikasi memberikan himbauan agar tidak memotret wajah manusia atau identitas pribadi.
- **Performa**: Waktu unggah foto dan penyimpanan tiket < 5 detik pada koneksi internet normal (4G/WiFi); waktu respons rekomendasi AI < 5 detik.
- **Ketersediaan & Fallback AI**: Apabila kuota API habis atau layanan AI tidak merespons, aplikasi tidak boleh mengalami *crash* dan secara otomatis mengaktifkan pemilihan kategori manual.
- **Keterjelasan (*Explainability*)**: Setiap hasil dari AI diberi label *"Saran AI"* disertai skor keyakinan (*confidence score*) dan deskripsi alasan.
- **Kemudahan Antarmuka**: Desain UI minimalis, kontras warna jelas, serta navigasi intuitif.

---

## 6. Model Data Awal (*Data Schema*)

### Entitas: `User`
- `id`: String (UID Firebase)
- `nama`: String
- `email`: String
- `peran`: Enum (`mahasiswa`, `petugas`)

### Entitas: `Category`
- `id`: String
- `nama`: String (contoh: *Kursi*, *Meja*, *AC*, *Proyektor*, *Pintu & Jendela*, *Kelistrikan/Lampu*, *Sanitasi*, *Lainnya*)

### Entitas: `Ticket`
- `id`: String
- `reporter_id`: String (relasi ke `User`)
- `gedung`: String
- `ruangan`: String
- `deskripsi`: String
- `category_id`: String (relasi ke `Category`)
- `status`: Enum (`baru`, `diverifikasi`, `diproses`, `selesai`, `ditolak`)
- `photo_url`: String
- `ai_suggested_category`: String (opsional)
- `ai_confidence`: Float (opsional)
- `created_at`: Timestamp
- `updated_at`: Timestamp

### Entitas: `StatusLog`
- `id`: String
- `ticket_id`: String (relasi ke `Ticket`)
- `status_sebelumnya`: String
- `status_baru`: String
- `diubah_oleh`: String (relasi ke `User`)
- `catatan_petugas`: String
- `timestamp`: Timestamp
