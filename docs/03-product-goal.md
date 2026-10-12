# 03. Product Goal — Student Facility Reporting

Dokumen ini mendefinisikan sasaran utama (*Product Goal*) yang ingin dicapai melalui pengembangan aplikasi Student Facility Reporting.

---

## 🎯 Pernyataan Product Goal (1 Kalimat Utama)

> **"Membantu mahasiswa melaporkan kerusakan fasilitas kampus dengan cepat dan mempermudah petugas menerima laporan yang terkategori secara konsisten, dengan AI sebagai pendukung keputusan awal, bukan pengambil keputusan final."**

---

## 💎 Nilai Utama Produk (*Value Proposition*)

1. **Bagi Mahasiswa (Pelapor)**:
   - **Efisiensi Waktu**: Pelaporan dapat diselesaikan dalam waktu kurang dari 2 menit (cukup ambil foto, pilih lokasi, konfirmasi saran kategori).
   - **Transparansi**: Mengetahui status penanganan laporan secara nyata (*real-time*).
   - **Kemudahan**: Tidak perlu bingung memilih taksonomi kategori teknis karena dibantu oleh saran AI Vision.

2. **Bagi Petugas Fasilitas (Pengelola)**:
   - **Kerapian Data**: Tiket masuk otomatis terstandarisasi ke dalam kategori fasilitas yang baku (misal: Kursi, Meja, AC, Proyektor, Kelistrikan).
   - **Prioritas Jelas**: Penanganan fasilitas yang rusak parah atau berada di ruangan perkuliahan penting dapat diprioritaskan lebih cepat.
   - **Kendali Penuh**: Petugas memiliki hak penuh untuk mengoreksi kategori dan mencatat progres penanganan perbaikan.

---

## 📊 Indikator Kunci Kesuksesan (Success Metrics)

- **Kecepatan Pelaporan**: Waktu pengisian laporan oleh mahasiswa rata-rata < 2 menit.
- **Akurasi Saran AI**: Minimal 70% akurasi deteksi kategori awal pada sampel 20–30 foto kerusakan kampus.
- **Tingkat Adopsi Saran AI**: Minimal 60% saran AI diterima langsung oleh pelapor tanpa perlu perubahan manual.
- **Verifikasi Petugas**: 100% tiket terverifikasi kategorinya sebelum dialihkan ke status *"Diproses"*.
- **Ketersediaan Layanan (*Graceful Fallback*)**: 100% sistem tetap berfungsi untuk membuat laporan secara manual ketika layanan AI Vision offline.
