# 07. AI Hypothesis & Specification — Student Facility Reporting

Dokumen ini mendefinisikan hipotesis pemanfaatan kecerdasan buatan (*AI Hypothesis*), alasan teknis pemilihan AI, struktur input-output data, penanganan kegagalan (*failure handling*), dan batasan sistem.

---

## 🤖 1. AI Hypothesis Canvas: AI-1 (Klasifikasi Visual Fasilitas)

| Aspek | Pertanyaan Kunci | Rincian Spesifikasi |
| :--- | :--- | :--- |
| **Masalah AI** | *Masalah apa yang dibantu oleh AI?* | Pengenalan visual objek dan indikasi kerusakan dari foto fasilitas kampus (misal: kursi patah, meja retak, AC bocor/bermasalah, proyektor mati) guna menghasilkan rekomendasi kategori fasilitas awal yang seragam dan konsisten. |
| **Alasan Bukan If-Else** | *Mengapa bukan menggunakan aturan percabangan (if-else) biasa?* | Citra foto bersifat tidak terstruktur (*unstructured data*). Kondisi pencahayaan, sudut pengambilan gambar (*angle*), variasi model perabot, dan jenis kerusakan sangat beragam sehingga mustahil dipetakan menggunakan aturan berbasis teks/if-else. Pilihan manual bebas oleh pengguna terbukti menghasilkan penamaan yang tidak seragam (masalah utama proyek ini). |
| **Input AI** | *Apa data masukan yang dikirim ke AI?* | 1. **Gambar (Foto Kerusakan)** dalam format JPEG/PNG beresolusi terkompresi.<br>2. **Daftar Kategori Baku** kampus (*allowed categories*): `Kursi`, `Meja`, `AC`, `Proyektor`, `Kelistrikan/Lampu`, `Pintu & Jendela`, `Sanitasi/Toilet`, `Lainnya`.<br>3. *Optional*: Teks deskripsi singkat yang dimasukkan pengguna. |
| **Output AI** | *Apa keluaran yang dihasilkan AI?* | Objek data terstruktur dalam format **JSON** yang dapat divalidasi oleh aplikasi mobile, memuat: nama kategori rekomendasi, kondisi fisik yang teramati, nilai keyakinan (*confidence score* 0.0 – 1.0), dan alasan singkat. |
| **Penanganan Jika Salah** | *Apa yang terjadi jika AI keliru atau gagal?* | 1. **Ambang Batas Keyakinan (*Confidence Threshold*)**: Jika skor keyakinan < 0.60, sistem meminta pengguna memilih kategori secara manual.<br>2. **Hak Pengguna**: Mahasiswa dapat mengganti saran kategori sebelum tiket dikirim.<br>3. **Verifikasi Petugas**: Petugas fasilitas dapat memvalidasi atau merevisi kategori saat tiket diproses.<br>4. **Graceful Fallback**: Jika koneksi API gagal/timeout (> 5 detik), form beralih otomatis ke seleksi manual tanpa memblokir pengiriman tiket. |

---

## 📄 2. Contoh Format Kontrak JSON Output AI

```json
{
  "ticket_id": "temp_preview_001",
  "suggestions": [
    {
      "category": "Kursi",
      "condition": "kaki kursi patah / lepas",
      "confidence": 0.88
    }
  ],
  "detected_objects": ["chair", "broken leg", "classroom floor"],
  "explanation": "Terdeteksi kursi perkuliahan dengan kerusakan pada bagian kaki penyangga."
}
```

---

## 🛡️ 3. Batasan Resmi AI (*AI Scope & Boundaries*)

1. **Saran, Bukan Eksekusi Otomatis**: Hasil rekomendasi AI adalah draf pembantu dan tidak pernah menjadi keputusan final tanpa konfirmasi manusia.
2. **Keterbatasan Visual**: AI rentan mengalami penurunan akurasi pada foto yang:
   - Terlalu gelap atau mengalami *motion blur*.
   - Mengambil objek dari jarak yang terlalu jauh.
   - Menampilkan banyak objek berbeda dalam satu *frame*.
3. **Privasi & Etika Data**:
   - Sistem tidak melakukan deteksi wajah (*face recognition*).
   - Pengguna dihimbau hanya memotret objek fisik fasilitas, bukan orang di sekitar.
4. **Independensi Fitur Inti**: Kegagalan fungsi AI tidak boleh menghentikan fungsi inti aplikasi (pembuatan tiket, unggah foto, dan penyimpanan data ke database).
