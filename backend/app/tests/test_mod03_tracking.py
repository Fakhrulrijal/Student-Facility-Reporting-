import sys
import os
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

backend_path = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(backend_path))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def run_tests():
    print("=" * 60)
    print("🚀 MENJALANKAN PENGUJIAN OTOMATIS MOD-03: TRACKING & HISTORI")
    print("=" * 60)

    import uuid
    uid = uuid.uuid4().hex[:6]
    nim_test = f"12{uid[:6]}"
    # Pastikan numerik 8 digit
    nim_test = f"{int(uuid.uuid4().int % 90000000 + 10000000)}"

    # 1. Pastikan ada user terdaftar dan buat laporan untuk user tersebut
    res_reg = client.post("/api/v1/auth/register", json={
        "nama": "Andrean Tracking",
        "nomor_induk": nim_test,
        "email": f"andrean.{uid}@kampus.ac.id",
        "password": "password123",
        "role": "Mahasiswa"
    })
    token = res_reg.json()["access_token"]
    user_id = res_reg.json()["user"]["id_user"]

    # 2. Buat laporan #1
    sample_img = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xFF\xDB\x00C\x00"
    files = {"foto": ("kursi_rusak.jpg", sample_img, "image/jpeg")}
    form1 = {
        "lokasi": "Ruang A002 – Gedung A",
        "kategori": "Kursi",
        "tingkat_keparahan": "Sedang",
        "deskripsi": "Sandaran kursi patah saat dipakai, berbahaya untuk mahasiswa.",
        "kode_qr": "KR-A002-07"
    }
    res_laporan1 = client.post("/api/v1/laporan", data=form1, files=files, headers={"Authorization": f"Bearer {token}"})
    assert res_laporan1.status_code == 201
    lap1 = res_laporan1.json()
    id_lap1 = lap1["id_laporan"]
    tiket1 = lap1["nomor_tiket"]
    print(f"✅ Pembuatan Tiket Uji {tiket1} (ID: {id_lap1}): OK")

    # 3. Test Endpoint GET /api/v1/laporan/user/{id_user}
    res_user_reports = client.get(f"/api/v1/laporan/user/{user_id}")
    assert res_user_reports.status_code == 200
    user_reps = res_user_reports.json()
    assert len(user_reps) >= 1
    assert user_reps[0]["id_laporan"] == id_lap1
    print(f"✅ GET /api/v1/laporan/user/{user_id} berhasil mengambil {len(user_reps)} laporan: OK")

    # 4. Test Filter Status di user reports
    res_filter_diajukan = client.get(f"/api/v1/laporan/user/{user_id}?status_filter=Diajukan")
    assert res_filter_diajukan.status_code == 200
    assert len(res_filter_diajukan.json()) >= 1
    print("✅ Filter status 'Diajukan' berhasil: OK")

    res_filter_selesai = client.get(f"/api/v1/laporan/user/{user_id}?status_filter=Selesai")
    assert res_filter_selesai.status_code == 200
    assert len(res_filter_selesai.json()) == 0
    print("✅ Filter status 'Selesai' (Empty State test): OK")

    # 5. Test Endpoint GET /api/v1/laporan/{id_laporan}/history (Slide 16 Mockup Timeline)
    res_hist = client.get(f"/api/v1/laporan/{id_lap1}/history")
    assert res_hist.status_code == 200
    hist_data = res_hist.json()
    assert hist_data["status_saat_ini"] == "Diajukan"
    assert len(hist_data["timeline"]) == 4

    # Tahap 1: Diajukan harus completed
    stage_diajukan = hist_data["timeline"][0]
    assert stage_diajukan["stage_name"] == "Diajukan"
    assert stage_diajukan["is_completed"] is True
    assert stage_diajukan["is_current"] is True

    # Tahap 2: Ditinjau Admin menunggu
    stage_tinjau = hist_data["timeline"][1]
    assert stage_tinjau["stage_name"] == "Ditinjau Admin"
    assert stage_tinjau["is_completed"] is False
    print("✅ Rincian 4 Tahap Timeline Vertikal (/history): OK")

    # 6. Test Update Status menjadi 'Diproses' dengan catatan teknisi (Slide 21 Mockup)
    res_update_diproses = client.put(f"/api/v1/laporan/{id_lap1}/status", json={
        "status": "Diproses",
        "catatan": "Sandaran akan diperbaiki teknisi pada hari Senin.",
        "updated_by": "Teknisi Budi"
    })
    assert res_update_diproses.status_code == 200
    assert res_update_diproses.json()["status"] == "Diproses"
    print("✅ Update status ke 'Diproses' dengan catatan teknisi: OK")

    # 7. Verifikasi Timeline setelah update ke 'Diproses'
    res_hist_updated = client.get(f"/api/v1/laporan/{id_lap1}/history")
    hist_data2 = res_hist_updated.json()
    assert hist_data2["status_saat_ini"] == "Diproses"
    stage_diproses = hist_data2["timeline"][2]
    assert stage_diproses["is_completed"] is True
    assert stage_diproses["is_current"] is True
    assert "Sandaran akan diperbaiki" in stage_diproses["catatan"]
    print("✅ Verifikasi pembaruan timeline status live ke 'Diproses': OK")

    # 8. Test Update Status menjadi 'Selesai'
    res_update_selesai = client.put(f"/api/v1/laporan/{id_lap1}/status", json={
        "status": "Selesai",
        "catatan": "Perbaikan kursi selesai dilakukan dan sudah layak digunakan kembali.",
        "updated_by": "Teknisi Budi"
    })
    assert res_update_selesai.status_code == 200
    assert res_update_selesai.json()["status"] == "Selesai"

    # Verifikasi filter 'Selesai' sekarang memiliki 1 tiket
    res_filter_selesai2 = client.get(f"/api/v1/laporan/user/{user_id}?status_filter=Selesai")
    assert len(res_filter_selesai2.json()) == 1
    print("✅ Update status ke 'Selesai' & verifikasi tab Selesai: OK")

    print("\n" + "=" * 60)
    print("🎉 SEMUA PENGUJIAN MOD-03 LULUS DENGAN SUKSES! (100% PASS)")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
