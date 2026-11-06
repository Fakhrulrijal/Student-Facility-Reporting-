import sys
import os
import uuid
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

backend_path = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(backend_path))

from fastapi.testclient import TestClient
from main import app
from app.database.json_db import db

client = TestClient(app)

def run_tests():
    print("=" * 60)
    print("🚀 MENJALANKAN PENGUJIAN OTOMATIS MOD-04: DASHBOARD ADMIN & KELOLA TIKET")
    print("=" * 60)

    # 1. Pastikan ada laporan sample yang siap dievaluasi
    sample_img = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xFF\xDB\x00C\x00"
    files = {"foto": ("kursi_patah.jpg", sample_img, "image/jpeg")}
    form = {
        "lokasi": "Ruang A002 – Gedung A",
        "kategori": "Kursi",
        "tingkat_keparahan": "Sedang",
        "deskripsi": "Sandaran kursi patah saat dipakai, berbahaya untuk mahasiswa.",
        "kode_qr": "KR-A002-07"
    }
    res_laporan = client.post("/api/v1/laporan", data=form, files=files)
    assert res_laporan.status_code == 201
    lap = res_laporan.json()
    id_lap = lap["id_laporan"]
    tiket_no = lap["nomor_tiket"]
    print(f"✅ Tiket Uji Laporan Masuk Terbuat: {tiket_no} (Status: Diajukan): OK")

    # 2. Test Endpoint GET /api/v1/admin/dashboard/summary
    res_summary = client.get("/api/v1/admin/dashboard/summary")
    assert res_summary.status_code == 200
    summary = res_summary.json()
    assert summary["total_laporan"] >= 1
    assert "breakdown_kategori" in summary
    assert "Kursi" in summary["breakdown_kategori"]
    print(f"✅ GET /api/v1/admin/dashboard/summary (Total: {summary['total_laporan']}, Menunggu: {summary['menunggu_peninjauan']}): OK")

    # 3. Test Endpoint GET /api/v1/admin/laporan
    res_admin_list = client.get("/api/v1/admin/laporan")
    assert res_admin_list.status_code == 200
    admin_list = res_admin_list.json()
    assert admin_list["total_laporan"] >= 1
    assert any(r["id_laporan"] == id_lap for r in admin_list["laporan"])
    print(f"✅ GET /api/v1/admin/laporan (List {len(admin_list['laporan'])} tiket aktif): OK")

    # 4. Test Skenario Evaluasi Layak (Terima & Tentukan Tindakan: Perbaiki -> Diproses)
    res_update_terima = client.put(f"/api/v1/admin/laporan/{id_lap}/status", json={
        "status": "Diproses",
        "aksi_teknis": "Perbaiki",
        "catatan": "Sandaran akan diperbaiki teknisi pada hari Senin.",
        "admin_id": "USR-002",
        "admin_name": "Administrator Fasilitas"
    })
    assert res_update_terima.status_code == 200
    update_res = res_update_terima.json()
    assert update_res["status_baru"] == "Diproses"
    assert update_res["aksi_teknis"] == "Perbaiki"
    assert "Sandaran akan diperbaiki" in update_res["catatan"]
    assert update_res["notification"]["success"] is True
    print(f"✅ Evaluasi Tiket Layak -> Status 'Diproses' (Aksi: Perbaiki) + FCM Push Notification: OK")

    # 5. Verifikasi Catatan di Database TINDAKAN_PENANGANAN
    data = db.load_data()
    tindakan_list = data.get("TINDAKAN_PENANGANAN", [])
    assert any(t["id_laporan"] == id_lap and t["aksi_teknis"] == "Perbaiki" for t in tindakan_list)
    print("✅ Verifikasi Entitas Relasi TINDAKAN_PENANGANAN tersimpan di JSON DB: OK")

    # 6. Test Skenario Evaluasi Tidak Layak (Tolak Laporan)
    # 6.1 Validasi Gagal: Tolak tanpa alasan wajib
    form2 = {
        "lokasi": "Ruang B101 – Gedung B",
        "kategori": "Proyektor",
        "tingkat_keparahan": "Ringan",
        "deskripsi": "Remot proyektor baterai habis."
    }
    res_lap2 = client.post("/api/v1/laporan", data=form2, files={"foto": ("proyektor.jpg", sample_img, "image/jpeg")})
    id_lap2 = res_lap2.json()["id_laporan"]

    res_tolak_invalid = client.put(f"/api/v1/admin/laporan/{id_lap2}/status", json={
        "status": "Ditolak",
        "alasan_penolakan": "" # Empty alasan
    })
    assert res_tolak_invalid.status_code == 400
    print("✅ Validasi Penolakan Wajib Mengisi Alasan (HTTP 400): OK")

    # 6.2 Tolak Laporan dengan Alasan Lengkap
    alasan = "Laporan duplikat — kerusakan yang sama sudah dilaporkan pada tiket #TK-0009."
    res_tolak_valid = client.put(f"/api/v1/admin/laporan/{id_lap2}/status", json={
        "status": "Ditolak",
        "alasan_penolakan": alasan,
        "admin_id": "USR-002",
        "admin_name": "Administrator Fasilitas"
    })
    assert res_tolak_valid.status_code == 200
    tolak_res = res_tolak_valid.json()
    assert tolak_res["status_baru"] == "Ditolak"
    assert tolak_res["alasan_penolakan"] == alasan
    assert tolak_res["notification"]["success"] is True
    assert "ditolak" in tolak_res["notification"]["body"].lower()
    print("✅ Penolakan Laporan dengan Alasan & Pengiriman Notifikasi ke Pelapor: OK")

    print("\n" + "=" * 60)
    print("🎉 SEMUA PENGUJIAN MOD-04 LULUS DENGAN SUKSES! (100% PASS)")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
