# 06. Role Assignment & Alur Kolaborasi Tim — Student Facility Reporting

Dokumen ini mendefinisikan pembagian peran tim berbasis model **Hacker – Hipster – Hustler**, ruang lingkup tanggung jawab masing-masing anggota, serta format evaluasi harian (*Daily Scrum*).

---

## 👥 1. Struktur Pembagian Peran Tim

| Peran | Nama Anggota | Ruang Lingkup Utama |
| :--- | :--- | :--- |
| **Hacker** | **Fakhrulrijal** | - Pengelolaan Repositori GitHub (Branching, Commit, PR, Issue templates)<br>- Arsitektur sistem dan konfigurasi proyek mobile (Flutter)<br>- Integrasi Backend & Database (Firebase Auth, Firestore, Storage)<br>- Implementasi integrasi API AI Vision (Google Gemini Vision API) |
| **Hipster** | **Muhammad** | - Riset kebutuhan dan alur pengalaman pengguna (UX research)<br>- Pembuatan wireframe dan prototipe UI antarmuka mobile<br>- Konsistensi sistem desain (warna, tipografi, komponen kartu laporan)<br>- Pengujian antarmuka aplikasi dengan pengguna |
| **Hustler** | **Roni** | - Perumusan problem statement dan penyelarasan nilai produk kampus<br>- Penentuan prioritas backlog dan pengawalan sprint goal<br>- Perumusan hipotesis AI, batasan, dan metrik akurasi solusi<br>- Dokumentasi kebutuhan bisnis dan presentasi proyek |

---

## 📊 2. Contoh Tabel Rapat Daily Scrum (Sesuai Slide Praktikum)

Berikut adalah catatan standup harian (*Daily Scrum*) tim untuk memastikan transparansi dan mengatasi kendala (*blocker*):

| Anggota | Sudah Dilakukan | Akan Dilakukan | Blocker / Kendala |
| :--- | :--- | :--- | :--- |
| **Hacker**<br>(Fakhrulrijal) | - Memetakan entitas data dan skema database Firebase<br>- Menyiapkan template issue dan PR di GitHub | - Membuat draft konfigurasi proyek Flutter<br>- Menyiapkan modul pemanggilan Gemini Vision API | Belum disepakati format JSON schema output AI Vision secara final |
| **Hipster**<br>(Muhammad) | - Membuat sketsa/wireframe layar Beranda dan Form Laporan<br>- Menentukan palet warna aplikasi | - Membuat user flow navigasi dari pemilihan foto hingga tiket terkirim | Belum ada keputusan navigasi detail status tiket untuk peran petugas |
| **Hustler**<br>(Roni) | - Menyusun AI Hypothesis awal dan batasan hasil klasifikasi<br>- Menyusun 12 item Product Backlog (MoSCoW) | - Menyusun daftar pertanyaan wawancara untuk 5 responden pengguna | Menunggu konfirmasi daftar kategori baku fasilitas yang diizinkan kampus |

---

## 📋 3. Matriks Tanggung Jawab Artefak (Pertemuan 1)

| Artefak | Penanggung Jawab Utama | Kontributor Pendukung |
| :--- | :--- | :--- |
| **Project Brief** | Seluruh Tim | Roni, Muhammad, Fakhrulrijal |
| **Problem Statement** | **Roni (Hustler)** | Seluruh Tim |
| **Product Goal** | Seluruh Tim | Roni, Muhammad, Fakhrulrijal |
| **Initial Backlog** | Seluruh Tim | Roni (Lead Backlog), Fakhrulrijal, Muhammad |
| **Role Assignment** | Seluruh Tim | Fakhrulrijal, Muhammad, Roni |
| **GitHub Repository** | **Fakhrulrijal (Hacker)** | Seluruh Tim |
| **AI Hypothesis** | **Roni (Hustler)** | Fakhrulrijal (Hacker) |
