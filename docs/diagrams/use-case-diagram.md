# Diagram Alur & Use Case — Student Facility Reporting

Dokumen ini memvisualisasikan interaksi aktor (Mahasiswa, Petugas Fasilitas, dan Sistem AI Vision) dengan sistem.

---

## 📊 Use Case Diagram (Mermaid)

```mermaid
flowchart LR
    subgraph Aktor
        M["Mahasiswa (Pelapor)"]
        P["Petugas Fasilitas"]
        AI["Google Gemini Vision API"]
    end

    subgraph "Aplikasi Student Facility Reporting"
        UC1(["Login & Logout"])
        UC2(["Isi Form & Ambil Foto Kerusakan"])
        UC3(["Analisis & Saran Kategori AI"])
        UC4(["Simpan Tiket Laporan (Status: Baru)"])
        UC5(["Lihat Riwayat & Status Tiket"])
        UC6(["Lihat Daftar Tiket Masuk"])
        UC7(["Verifikasi/Koreksi Kategori Tiket"])
        UC8(["Perbarui Status Tiket & Catatan"])
    end

    M --> UC1
    M --> UC2
    UC2 -.->|Kirim Foto| UC3
    AI -.->|Kembalikan JSON Saran| UC3
    UC3 -.->|Konfirmasi Kategori| UC4
    M --> UC4
    M --> UC5

    P --> UC1
    P --> UC6
    P --> UC7
    P --> UC8
```

---

## 🔄 Alur Pelaporan Mahasiswa (User Flow)

```mermaid
sequenceDiagram
    autonumber
    actor Mahasiswa
    participant App as Flutter Mobile App
    participant AI as Gemini Vision API
    participant DB as Cloud Firestore / Storage

    Mahasiswa->>App: Buka form laporan & ambil foto
    App->>AI: Kirim foto kerusakan untuk dianalisis
    AI-->>App: Respon JSON (Kategori, Kondisi, Confidence)
    App->>Mahasiswa: Tampilkan kartu rekomendasi AI
    Mahasiswa->>App: Konfirmasi/Ubah kategori & klik "Kirim"
    App->>DB: Simpan foto ke Storage & tiket ke Firestore (Status: Baru)
    DB-->>App: Tiket berhasil disimpan
    App->>Mahasiswa: Notifikasi sukses & tampilkan di daftar riwayat
```
