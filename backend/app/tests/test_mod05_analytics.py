import sys
import os
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
    print("🚀 MENJALANKAN PENGUJIAN OTOMATIS MOD-05: RANGKUMAN EKSEKUTIF AI")
    print("=" * 60)

    # 1. Pastikan ada data laporan untuk dianalisis
    sample_img = b"\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xFF\xDB\x00C\x00"
    for i in range(3):
        client.post("/api/v1/laporan", data={
            "lokasi": "Ruang A002 – Gedung A",
            "kategori": "Kursi",
            "tingkat_keparahan": "Sedang",
            "deskripsi": f"Uji analisis AI laporan kursi ke-{i+1}"
        }, files={"foto": (f"kursi_{i}.jpg", sample_img, "image/jpeg")})

    client.post("/api/v1/laporan", data={
        "lokasi": "Ruang B101 – Gedung B",
        "kategori": "Proyektor",
        "tingkat_keparahan": "Berat",
        "deskripsi": "Lampu proyektor mati saat kuliah umum."
    }, files={"foto": ("proyektor.jpg", sample_img, "image/jpeg")})

    print("✅ Penyiapan Data Laporan Sampel: OK")

    # 2. Test POST /api/v1/analytics/summary (Skenario Data Ditemukan - Slide 25 Mockup)
    res_summary = client.post("/api/v1/analytics/summary", json={
        "periode": "Semua Periode",
        "gedung": "Semua Gedung",
        "kategori": "Semua Kategori"
    })
    assert res_summary.status_code == 200, f"Error: {res_summary.text}"
    data_summary = res_summary.json()
    assert data_summary["found"] is True
    assert data_summary["total_laporan"] >= 4
    assert len(data_summary["bullets"]) >= 3
    assert len(data_summary["rekomendasi"]) > 10
    assert data_summary["id_analisis"] is not None
    print(f"✅ Generate Rangkuman Eksekutif AI Berhasil ({data_summary['id_analisis']}): OK")
    print(f"   - Pola 1: {data_summary['bullets'][0]}")
    print(f"   - Pola 2: {data_summary['bullets'][1]}")
    print(f"   - Pola 3: {data_summary['bullets'][2]}")
    print(f"   - Rekomendasi: {data_summary['rekomendasi']}")

    # 3. Test Skenario Filter Spesifik (Gedung A)
    res_gedung_a = client.post("/api/v1/analytics/summary", json={
        "periode": "Semua Periode",
        "gedung": "Gedung A",
        "kategori": "Semua Kategori"
    })
    assert res_gedung_a.status_code == 200
    assert res_gedung_a.json()["found"] is True
    print("✅ Filter Spesifik Gedung A: OK")

    # 4. Test Skenario Data Tidak Ditemukan (Slide 26 Mockup)
    res_not_found = client.post("/api/v1/analytics/summary", json={
        "periode": "Januari 2020",
        "gedung": "Gedung Antariksa",
        "kategori": "Helikopter"
    })
    assert res_not_found.status_code == 200
    not_found_data = res_not_found.json()
    assert not_found_data["found"] is False
    assert not_found_data["total_laporan"] == 0
    print("✅ Skenario Data Tidak Ditemukan (found=False & Pesan Panduan): OK")

    # 5. Test Riwayat Analisis AI GET /api/v1/analytics/history
    res_history = client.get("/api/v1/analytics/history")
    assert res_history.status_code == 200
    history_list = res_history.json()
    assert len(history_list) >= 1
    assert any(h["id_analisis"] == data_summary["id_analisis"] for h in history_list)
    print(f"✅ Verifikasi Entitas ANALISIS_AI Tersimpan di Database JSON (Total: {len(history_list)} riwayat): OK")

    print("\n" + "=" * 60)
    print("🎉 SEMUA PENGUJIAN MOD-05 LULUS DENGAN SUKSES! (100% PASS)")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
