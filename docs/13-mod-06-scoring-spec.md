# 13. MOD-06: Engine Prioritasi & Scoring Penanganan AI

Dokumen spesifikasi teknis untuk implementasi **Modul 6 (MOD-06)**: Engine Prioritasi Penanganan Fasilitas Kampus Berbasis Skor Urgensi AI (Google Gemini / Heuristik Komposit).

---

## 📌 Ruang Lingkup & Tujuan
Modul ini bertugas menyusun perangkingan cerdas (*intelligent automated ticket ranking*) untuk membantu petugas dan admin fasilitas memprioritaskan penanganan laporan kerusakan secara objektif, terukur, dan transparan.

---

## 🧮 Formula Algoritma Skor Urgensi (0–100)

Skor Urgensi dihitung berdasarkan komposit 3 variabel dengan bobot matematis:

$$\text{Skor Urgensi} = (0.40 \times S_{\text{keparahan}}) + (0.30 \times S_{\text{frekuensi}}) + (0.30 \times S_{\text{dampak}})$$

### 1. Keparahan Laporan ($S_{\text{keparahan}}$) — Bobot 40%
Nilai keparahan kerusakan fasilitas berdasarkan input pelapor dan validasi visual:
- **Berat / Tinggi**: Nilai $100$
- **Sedang**: Nilai $60$
- **Ringan / Rendah**: Nilai $30$

### 2. Frekuensi Pelaporan Aset / Gedung ($S_{\text{frekuensi}}$) — Bobot 30%
Frekuensi kerusakan pada aset/fasilitas yang sama atau di gedung/ruangan yang sama menunjukkan eskalasi masalah sistemik:
- Formula: $\min(100, \text{jumlah\_laporan\_terkait} \times 20)$
- Contoh: Jika ada $\ge 5$ laporan pada gedung/kategori serupa $\rightarrow 100$ poin.

### 3. Dampak Fasilitas terhadap Kegiatan Kampus ($S_{\text{dampak}}$) — Bobot 30%
Dihitung berdasarkan tingkat kekritisan fasilitas terhadap kegiatan belajar-mengajar dan keselamatan:
- **Fasilitas Vital / Kritis** (Listrik, AC Laboratorium/Ujian, Proyektor Kelas, Plafon Bocor): Nilai $90 - 100$
- **Fasilitas Penunjang Umum** (Toilet, Pintu, Jendela, Lampu Lorong): Nilai $70 - 80$
- **Fasilitas Non-Kritis / Individual** (Kursi, Meja, Papan Tulis Tambahan): Nilai $40 - 60$

---

## 🏷️ Klasifikasi Kategori Prioritas

| Kategori Prioritas | Rentang Skor | Warna Aksen | Tindakan Operasional |
| :--- | :---: | :---: | :--- |
| **Tinggi** | $> 80$ | 🔴 `#EF4444` (Merah) | Penanganan segera dalam $1 \times 24$ jam. |
| **Sedang** | $50 - 80$ | 🟡 `#F59E0B` (Kuning-Oranye) | Dijadwalkan perbaikan dalam $2 - 3$ hari kerja. |
| **Rendah** | $< 50$ | 🟢 `#10B981` (Hijau) | Pemeliharaan berkala / antrean rutin. |

---

## 🔌 Spesifikasi REST API Backend

### 1. `POST /api/v1/ai/prioritize-tickets`
Mengevaluasi seluruh laporan aktif, mengkalkulasi skor komposit, menyimpan ke tabel `ANALISIS_AI`, dan mengembalikan daftar tiket terurut ranking (#1, #2, dst.).

### 2. `GET /api/v1/ai/prioritized-tickets`
Mengambil data perangkingan tiket prioritas dengan filter opsional (`prioritas=Tinggi|Sedang|Rendah`, `kategori`, `gedung`).

### 3. `GET /api/v1/ai/prioritize-ticket/{id_laporan}`
Mengambil rincian breakdown pembobotan spesifik untuk satu tiket tertentu.

---

## 📱 Implementasi Frontend Flutter
- Layar **AdminPriorityScreen** pada tab `Prioritas` di `AdminNavigationShell`.
- Indikator visual kartu rangking dengan aksen warna urgensi tegas.
- Kartu breakdown komponen skor (Keparahan 40%, Frekuensi 30%, Dampak 30%).
- Tombol kalkulasi ulang prioritas (*Recalculate AI*).
- Tombol aksi "Tindak Lanjuti" yang terhubung langsung ke alur penanganan teknisi.
