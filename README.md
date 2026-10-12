# Student Facility Reporting

Aplikasi mobile pelaporan kerusakan fasilitas kampus berbasis kecerdasan buatan (*AI Vision*) untuk membantu standardisasi dan konsistensi kategorisasi laporan fasilitas sebelum diverifikasi oleh pengguna dan petugas kampus.

---

## 📌 Problem Statement (Sementara)

Mahasiswa yang menemukan fasilitas kampus rusak membutuhkan cara yang mudah dan seragam untuk melaporkannya, karena laporan dengan kategori yang ditulis bebas (misalnya *"kursi rusak"*, *"meja patah"*, *"AC bermasalah"*) sulit dikelompokkan dan diprioritaskan oleh petugas. Kondisi tersebut membuat penanganan menjadi lambat dan tidak konsisten. 

Aplikasi **Student Facility Reporting** menyediakan form laporan dengan unggah foto dan penyimpanan tiket status, serta saran kategori awal dari **AI Vision** yang diverifikasi oleh pengguna atau petugas agar laporan lebih rapi, terstruktur, dan cepat ditangani.

---

## 👥 Anggota Tim & Peran

| Nama | Peran | Fokus & Tanggung Jawab Utama |
| :--- | :--- | :--- |
| **Fakhrulrijal** | **Hacker** | Arsitektur kode, setup Git/repository, backend/autentikasi Firebase, dan integrasi Google Gemini Vision API. |
| **Muhammad** | **Hipster** | Riset kebutuhan pengguna, desain UI/UX, wireframe, alur navigasi mobile, serta pengujian antarmuka. |
| **Roni** | **Hustler** | Problem statement, validasi nilai produk, prioritas backlog, perumusan hipotesis AI, metrik keberhasilan, dan presentasi tim. |

---

## 🛠️ Teknologi yang Direncanakan

- **Mobile Framework**: [Flutter](https://flutter.dev/) (Dart) — Multiplatform Android & iOS
- **Backend & Database**: [Firebase](https://firebase.google.com/)
  - **Firebase Authentication**: Login & registrasi mahasiswa serta petugas fasilitas
  - **Cloud Firestore**: Database NoSQL realtime untuk tiket laporan dan status log
  - **Cloud Storage**: Penyimpanan foto bukti kerusakan fasilitas
- **AI Vision Service**: [Google Gemini Vision API](https://ai.google.dev/) — Menganalisis foto fasilitas untuk menyarankan kategori kerusakan awal secara terstruktur (JSON output)
- **Version Control**: Git & GitHub

---

## ⚠️ Batasan AI (*AI Scope & Boundaries*)

1. **Saran, Bukan Keputusan Final**: Output dari AI Vision berstatus *draft/suggestion*.
2. **Wajib Verifikasi Manusia**: Kategori akhir selalu dikonfirmasi oleh mahasiswa pelapor atau diverifikasi oleh petugas fasilitas kampus.
3. **Keterbatasan Kondisi Foto**: AI dapat menghasilkan akurasi rendah pada foto yang gelap, buram, atau memiliki terlalu banyak objek sekaligus.
4. **Resiliensi Fitur Utama (*Graceful Fallback*)**: Jika layanan AI mengalami kendala jaringan atau kegagalan API, pengguna tetap dapat memilih kategori secara manual tanpa menghambat proses pengiriman laporan.

---

## 📂 Dokumentasi Proyek

Dokumentasi lengkap proyek dapat dilihat di folder [`docs/`](./docs/):
- [`01-project-brief.md`](./docs/01-project-brief.md) — Ringkasan kebutuhan dan ruang lingkup MVP
- [`02-problem-statement.md`](./docs/02-problem-statement.md) — Definisi masalah dari sudut pandang pengguna
- [`03-product-goal.md`](./docs/03-product-goal.md) — Tujuan utama dan sasaran produk
- [`04-prd.md`](./docs/04-prd.md) — Dokumen Kebutuhan Produk (PRD) lengkap
- [`05-initial-backlog.md`](./docs/05-initial-backlog.md) — 12 User Story terurut prioritas (MoSCoW)
- [`06-role-assignment.md`](./docs/06-role-assignment.md) — Rincian tugas Hacker, Hipster, Hustler & Scrum Board
- [`07-ai-hypothesis.md`](./docs/07-ai-hypothesis.md) — Hipotesis, skema I/O JSON, dan mitigasi kegagalan AI
- [`decisions/ADR-0001-pilihan-teknologi.md`](./docs/decisions/ADR-0001-pilihan-teknologi.md) — Catatan keputusan arsitektur (ADR)
- [`research/pertanyaan-wawancara.md`](./docs/research/pertanyaan-wawancara.md) — Panduan wawancara 5 responden pengguna

---

## 🚀 Alur Berkontribusi (*Contribution Guide*)

Silakan baca panduan lengkap pada [CONTRIBUTING.md](./CONTRIBUTING.md) mengenai aturan branching (`main`, `develop`, `feature/*`), format pesan commit, dan pembuatan *Pull Request*.
