# Panduan Kontribusi Tim — Student Facility Reporting

Dokumen ini mengatur alur kerja tim agar kolaborasi di GitHub berjalan rapi, transparan, dan terstruktur.

---

## 🌿 1. Strategi Percabangan (Branching Strategy)

Tim menggunakan alur percabangan berbasis fitur:

- **`main`**:
  - Cabang utama untuk kode stabil yang siap diuji/rilis.
  - **DILARANG commit langsung ke `main`**. Semua perubahan wajib melalui *Pull Request* (PR).
- **`develop`**:
  - Cabang integrasi pengembangan fitur harian.
- **Cabang Dokumentasi & Fitur Baru**:
  - Format penamaan cabang:
    - Dokumentasi: `docs/<nama-dokumen>` (contoh: `docs/pertemuan-1-artefak`)
    - Fitur baru: `feature/US-<nomor>-<deskripsi-singkat>` (contoh: `feature/US-02-form-laporan`)
    - Perbaikan bug: `fix/<deskripsi-bug>` (contoh: `fix/upload-foto-timeout`)

---

## 💬 2. Konvensi Pesan Commit (Conventional Commits)

Format commit pesan:
`<type>: <deskripsi perubahan>`

Jenis (*type*) yang digunakan:
- `docs:` Perubahan atau penambahan pada dokumentasi (misal: `docs: tambah problem statement dan PRD`)
- `feat:` Penambahan fitur baru kode aplikasi (misal: `feat: implementasi form laporan US-02`)
- `fix:` Perbaikan bug kode aplikasi (misal: `fix: perbaiki validasi form login`)
- `refactor:` Pengubahan struktur kode tanpa mengubah fungsionalitas
- `chore:` Perubahan konfigurasi repositori, dependensi, atau `.gitignore`

---

## 🔀 3. Alur Kerja Pull Request (PR)

1. Buat branch baru dari `main` atau `develop`.
2. Lakukan perubahan file/kode dan commit dengan pesan yang jelas.
3. Push branch ke GitHub:
   ```bash
   git push origin <nama-branch>
   ```
4. Buka **Pull Request** di GitHub ke cabang target (`main` / `develop`).
5. Isi deskripsi PR menggunakan *template* PR yang telah disediakan.
6. Minta minimal satu anggota tim untuk melakukan *code review* dan *approve*.
7. Setelah disetujui, lakukan **Squash and Merge** atau **Rebase and Merge**.
8. Hapus branch fitur setelah PR berhasil di-merge.
