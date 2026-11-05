# Spesifikasi Teknis MOD-01: Autentikasi & User Management

## 📌 Ringkasan Modul
Modul ini mengimplementasikan autentikasi dan manajemen akun civitas akademika (Mahasiswa, Dosen, dan Admin) sesuai dengan **Diagram 1 Aktivitas UML** dan spesifikasi entitas `PENGGUNA` serta `DETAIL_AKUN`.

---

## 🛠️ REST API Endpoints (FastAPI)

### 1. Registrasi Akun
- **Endpoint**: `POST /api/v1/auth/register`
- **Request Body**:
```json
{
  "nama": "Fakhrul Rijal",
  "nomor_induk": "22095111",
  "email": "fakhrul@kampus.ac.id",
  "password": "secretPassword123",
  "role": "Mahasiswa",
  "fakultas": "Ilmu Komputer",
  "prodi": "Informatika"
}
```
- **Validation Rules**:
  - `nomor_induk` (NIM/NIP): Wajib numerik 8 digit (`^\d{8}$`).
  - `email`: Wajib menggunakan domain kampus `@kampus.ac.id`.
  - `password`: Minimal 8 karakter.
  - Duplikasi: Mengecek keunikan NIM dan email dalam basis data.
- **Response**: `201 Created` berisi JWT Token dan data profil pengguna.

### 2. Login Akun
- **Endpoint**: `POST /api/v1/auth/login`
- **Request Body**:
```json
{
  "nomor_induk_atau_email": "22095111",
  "password": "secretPassword123"
}
```
- **Response**: `200 OK` berisi JWT Access Token (Bearer).
- **Error Handling**: `401 Unauthorized` dengan pesan `"NIM / Email atau password salah. Silakan periksa kembali kredensial Anda."` jika kredensial tidak cocok.

### 3. Profil Pengguna Terproteksi
- **Endpoint**: `GET /api/v1/auth/me`
- **Header**: `Authorization: Bearer <TOKEN>`
- **Response**: Detail data identitas pengguna aktif.

---

## 📱 Implementasi Frontend (Flutter)
1. **`LoginScreen`** (`lib/screens/auth/login_screen.dart`):
   - Input NIM/NIP dan Password dengan toggle visibility.
   - Banner error validation & custom error dialog.
   - Tombol simulasi cepat (Mahasiswa Andrean, Admin Fasilitas, dan skenario login gagal).
2. **`RegisterScreen`** (`lib/screens/auth/register_screen.dart`):
   - Input Nama, NIM/NIP (8 digit validator), Email (@kampus.ac.id validator), Password, dan Pilihan Peran.
   - Skenario simulasi data tidak valid sesuai Slide 5 Mockup.
3. **State Management**: `AuthProvider` (`lib/providers/auth_provider.dart`) menggunakan pola Provider.
