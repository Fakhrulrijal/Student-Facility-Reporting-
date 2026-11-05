import sys
import os
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add backend directory to path
backend_path = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(backend_path))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def run_tests():
    print("=" * 60)
    print("🚀 MENJALANKAN PENGUJIAN OTOMATIS MOD-01 & MOD-02")
    print("=" * 60)

    # 1. Health check
    res = client.get("/")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("✅ Health check API: OK")

    # 2. MOD-01: Validasi Registrasi Akun
    print("\n--- TEST MOD-01: Registrasi & Autentikasi ---")
    
    # 2.1 Error: NIM bukan 8 digit
    res = client.post("/api/v1/auth/register", json={
        "nama": "Budi Santoso",
        "nomor_induk": "1234", # invalid
        "email": "budi@kampus.ac.id",
        "password": "password123",
        "role": "Mahasiswa"
    })
    assert res.status_code == 422, f"Expected 422 for short NIM, got {res.status_code}"
    print("✅ Validasi NIM < 8 digit tertolak (HTTP 422): OK")

    # 2.2 Error: Email bukan @kampus.ac.id
    res = client.post("/api/v1/auth/register", json={
        "nama": "Budi Santoso",
        "nomor_induk": "22010101",
        "email": "budi@gmail.com", # invalid
        "password": "password123",
        "role": "Mahasiswa"
    })
    assert res.status_code == 422, f"Expected 422 for non-kampus domain, got {res.status_code}"
    print("✅ Validasi Domain Email non-kampus tertolak (HTTP 422): OK")

    # 2.3 Error: Password < 8 karakter
    res = client.post("/api/v1/auth/register", json={
        "nama": "Budi Santoso",
        "nomor_induk": "22010101",
        "email": "budi@kampus.ac.id",
        "password": "short", # invalid
        "role": "Mahasiswa"
    })
    assert res.status_code == 422, f"Expected 422 for short password, got {res.status_code}"
    print("✅ Validasi Password < 8 karakter tertolak (HTTP 422): OK")

    # 2.4 Berhasil Registrasi Akun Mahasiswa Baru
    import uuid
    uid = uuid.uuid4().hex[:6]
    nim_new = f"{int(uuid.uuid4().int % 90000000 + 10000000)}"
    email_new = f"fakhrul.{uid}@kampus.ac.id"

    res = client.post("/api/v1/auth/register", json={
        "nama": "Fakhrul Rijal",
        "nomor_induk": nim_new,
        "email": email_new,
        "password": "secretPassword123",
        "role": "Mahasiswa",
        "fakultas": "Ilmu Komputer",
        "prodi": "Informatika"
    })
    assert res.status_code == 201, f"Expected 201 for valid register, got {res.status_code}: {res.text}"
    reg_data = res.json()
    assert "access_token" in reg_data
    token = reg_data["access_token"]
    print("✅ Registrasi Mahasiswa Baru & Penerbitan JWT Token: OK")

    # 2.5 Error: Duplikasi Registrasi
    res_dup = client.post("/api/v1/auth/register", json={
        "nama": "Fakhrul Rijal Clone",
        "nomor_induk": nim_new,
        "email": email_new,
        "password": "secretPassword123",
        "role": "Mahasiswa"
    })
    assert res_dup.status_code == 400, f"Expected 400 for duplicate user, got {res_dup.status_code}"
    print("✅ Pencegahan Duplikasi NIM & Email (HTTP 400): OK")

    # 2.6 Login Gagal (Password salah)
    res_fail = client.post("/api/v1/auth/login", json={
        "nomor_induk_atau_email": nim_new,
        "password": "wrongPassword"
    })
    assert res_fail.status_code == 401, f"Expected 401 for wrong password, got {res_fail.status_code}"
    print("✅ Skenario Login Gagal (HTTP 401 Kredensial Salah): OK")

    # 2.7 Login Berhasil dengan NIM
    res_login = client.post("/api/v1/auth/login", json={
        "nomor_induk_atau_email": nim_new,
        "password": "secretPassword123"
    })
    assert res_login.status_code == 200
    assert res_login.json()["user"]["nama"] == "Fakhrul Rijal"
    print("✅ Login Berhasil via NIM & Verifikasi Bcrypt: OK")

    # 2.8 Login Berhasil dengan Email
    res_login_email = client.post("/api/v1/auth/login", json={
        "nomor_induk_atau_email": email_new,
        "password": "secretPassword123"
    })
    assert res_login_email.status_code == 200
    print("✅ Login Berhasil via Email Kampus: OK")

    # 2.9 Akses Profil Terproteksi via Bearer Token
    res_me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res_me.status_code == 200
    assert res_me.json()["nomor_induk"] == nim_new
    print("✅ Akses Protected Route (/api/v1/auth/me) via JWT: OK")

    # 3. MOD-02: Pelaporan Kerusakan & QR Scanner
    print("\n--- TEST MOD-02: Pelaporan Kerusakan & QR Scanner ---")

    # 3.1 QR Scanner: Scan QR Terdaftar (KR-A002-07)
    res_qr = client.get("/api/v1/fasilitas/qr/KR-A002-07")
    assert res_qr.status_code == 200, f"QR scan failed: {res_qr.text}"
    qr_data = res_qr.json()
    assert qr_data["kategori"] == "Kursi"
    assert "Ruang A002 – Gedung A" in qr_data["lokasi_gedung"]
    print("✅ Scan QR Terdaftar (KR-A002-07) -> Auto-fill Lokasi & Kategori: OK")

    # 3.2 QR Scanner: Scan QR Tidak Dikenali (Fallback scenario)
    res_qr_invalid = client.get("/api/v1/fasilitas/qr/UNKNOWN-999")
    assert res_qr_invalid.status_code == 404, f"Expected 404 for unknown QR, got {res_qr_invalid.status_code}"
    print("✅ Skenario QR Tidak Dikenali (HTTP 404 & Pesan Panduan Fallback): OK")

    # 3.3 Pengajuan Laporan Kerusakan Baru (Multipart Form Data dengan Upload Foto)
    sample_img_content = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xFF\xDB\x00C\x00"  # Dummy JPEG header
    files = {
        "foto": ("kursi_rusak.jpg", sample_img_content, "image/jpeg")
    }
    form_data = {
        "lokasi": "Ruang A002 – Gedung A",
        "kategori": "Kursi",
        "tingkat_keparahan": "Sedang",
        "deskripsi": "Sandaran kursi patah saat dipakai, berbahaya untuk mahasiswa.",
        "kode_qr": "KR-A002-07"
    }
    headers = {"Authorization": f"Bearer {token}"}

    res_report = client.post("/api/v1/laporan", data=form_data, files=files, headers=headers)
    assert res_report.status_code == 201, f"Failed to submit report: {res_report.text}"
    report_res = res_report.json()
    assert report_res["status"] == "Diajukan"
    assert report_res["nomor_tiket"].startswith("#TK-")
    assert "/uploads/" in report_res["foto_url"]
    print(f"✅ Pengajuan Laporan Baru Berhasil: Tiket {report_res['nomor_tiket']} diterbitkan (Status: Diajukan): OK")

    # 3.4 Ambil Daftar Laporan
    res_list = client.get("/api/v1/laporan")
    assert res_list.status_code == 200
    reports = res_list.json()
    assert len(reports) >= 1
    assert reports[0]["nomor_tiket"] == report_res["nomor_tiket"]
    print(f"✅ Pengambilan Daftar Histori Laporan (Total {len(reports)} laporan): OK")

    # 3.5 Ambil Rincian Laporan berdasarkan ID / Nomor Tiket
    res_detail = client.get(f"/api/v1/laporan/{report_res['id_laporan']}")
    assert res_detail.status_code == 200
    assert res_detail.json()["kategori"] == "Kursi"
    print(f"✅ Pengambilan Detail Laporan ({report_res['nomor_tiket']} / {report_res['id_laporan']}): OK")

    print("\n" + "=" * 60)
    print("🎉 SEMUA TEST MOD-01 DAN MOD-02 LULUS DENGAN SUKSES! (100% PASS)")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
