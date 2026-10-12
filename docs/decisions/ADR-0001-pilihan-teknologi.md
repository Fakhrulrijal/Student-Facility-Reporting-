# ADR-0001: Pemilihan Tumpukan Teknologi Aplikasi Mobile

**Status**: Diterima (Accepted)  
**Tanggal**: 2026-10-12  
**Pengambil Keputusan**: Fakhrulrijal (Hacker), Muhammad (Hipster), Roni (Hustler)  

---

## 1. Konteks Masalah
Proyek Student Facility Reporting membutuhkan pengembangan aplikasi mobile yang:
1. Mendukung pengambilan foto kamera dan antarmuka responsif di perangkat mobile.
2. Memerlukan autentikasi pengguna, penyimpanan data dokumen tiket, dan penyimpanan berkas media foto.
3. Memerlukan layanan model AI Vision yang dapat menerima input gambar dan menghasilkan keluaran teks terstruktur (JSON) dengan latensi rendah.
4. Memiliki waktu pengembangan cepat (*rapid prototyping*) dalam kurun waktu satu semester praktikum.

---

## 2. Alternatif yang Dipertimbangkan

### Opsi 1: Flutter + Firebase + Google Gemini Vision API
- **Kelebihan**:
  - Flutter memiliki ekosistem widget kaya dan performa native tinggi di Android/iOS dengan satu basis kode Dart.
  - Firebase menyediakan solusi all-in-one (Auth, Firestore, Cloud Storage) tanpa perlu membangun REST API backend dari nol.
  - Google Gemini 1.5 Flash / Gemini Vision sangat cepat dalam analisis multimodal foto dan mendukung *Structured JSON Output*.
- **Kekurangan**:
  - Ukuran binary awal Flutter sedikit lebih besar.

### Opsi 2: React Native + Supabase + OpenAI GPT-4o-mini
- **Kelebihan**:
  - Basis JavaScript/TypeScript familiar bagi web developer.
  - Supabase berbasis PostgreSQL dengan dukungan SQL langsung.
- **Kekurangan**:
  - Konfigurasi kamera native di React Native sering membutuhkan dependensi native tambahan yang kompleks.

---

## 3. Keputusan
Tim menyepakati penggunaan **Opsi 1**:
- **Mobile Framework**: **Flutter (Dart)**
- **Backend & Database**: **Firebase (Authentication, Cloud Firestore, Cloud Storage)**
- **AI Vision Engine**: **Google Gemini Vision API (Multimodal)**

---

## 4. Konsekuensi & Mitigasi
- **Konsekuensi**: Ketergantungan pada koneksi API Google Gemini dan kuota penggunaan.
- **Mitigasi**: Menerapkan mekanisme *graceful fallback* di mana pengguna tetap dapat memilih kategori secara manual jika API AI mengalami gangguan jaringan atau kuota habis.
