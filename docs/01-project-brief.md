# 01. Project Brief — Student Facility Reporting

Dokumen ini memuat ikhtisar tingkat tinggi mengenai inisiatif proyek aplikasi mobile pelaporan fasilitas kampus.

---

## 📌 Informasi Dasar Proyek

| Elemen | Keterangan |
| :--- | :--- |
| **Nama Proyek** | **Student Facility Reporting** |
| **Kasus Proyek** | Kasus 2 — Student Facility Reporting |
| **Fokus Masalah** | Laporan fasilitas rusak seringkali ditulis dengan penamaan kategori yang tidak seragam (misal: "kursi rusak", "meja patah", "AC bermasalah"), sehingga sulit dikelompokkan dan diprioritaskan secara konsisten oleh petugas. |
| **Pengguna Utama** | 1. **Mahasiswa** (pelapor fasilitas rusak di kampus)<br>2. **Petugas Fasilitas** (penerima, verifikator, dan penindaklanjut tiket) |
| **Tujuan Proyek** | Mahasiswa dapat melaporkan kerusakan fasilitas kampus secara cepat dan mudah melalui ponsel (foto, lokasi, deskripsi), serta petugas menerima tiket dengan kategori yang rapi, terstruktur, dan konsisten. |
| **Data Awal** | Akun pengguna, foto bukti, data lokasi (gedung/ruangan), deskripsi teks, kategori fasilitas, status tiket, log riwayat. |

---

## 🎯 Ruang Lingkup MVP (*Minimum Viable Product*)

1. **Autentikasi Pengguna**: Login dan logout untuk peran Mahasiswa dan Petugas Fasilitas.
2. **Formulir Pelaporan**: Pengisian lokasi kerusakan, deskripsi masalah, dan pemilihan kategori.
3. **Unggah Foto Kerusakan**: Pengambilan gambar secara langsung melalui kamera atau galeri ponsel dengan pratinjau.
4. **Prototipe AI Vision**: Rekomendasi/saran kategori awal otomatis berbasis foto kerusakan sebelum tiket dikirim.
5. **Penyimpanan Tiket & Status**: Tiket tersimpan dengan status awal `"baru"` beserta riwayat perubahan status.
6. **Manajemen Tiket**:
   - Tampilan daftar dan detail tiket milik mahasiswa.
   - Tampilan daftar tiket masuk bagi petugas fasilitas untuk verifikasi kategori dan pembaruan status penanganan.

---

## ⚠️ Batasan & Prinsip AI

- Hasil analisis AI berstatus **saran/draft awal**, bukan keputusan final.
- Kategori akhir selalu dapat diubah oleh mahasiswa pelapor atau diverifikasi oleh petugas fasilitas kampus.
- Jika layanan AI gagal atau foto tidak jelas, aplikasi tetap dapat digunakan dengan pemilihan kategori manual (*graceful fallback*).
