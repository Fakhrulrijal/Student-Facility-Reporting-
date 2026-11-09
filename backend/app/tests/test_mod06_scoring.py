import sys
import unittest
from pathlib import Path

# Pastikan console Windows encoding UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

backend_path = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(backend_path))

from fastapi.testclient import TestClient
from main import app
from app.database.json_db import db
from app.core.gemini_service import gemini_analytics

client = TestClient(app)

class TestMod06Scoring(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n" + "=" * 60)
        print("🚀 MENJALANKAN PENGUJIAN OTOMATIS MOD-06: ENGINE PRIORITAS & SCORING AI")
        print("=" * 60)

    def test_01_healthcheck_mod06_active(self):
        """Memastikan MOD-06 terdaftar di health check backend"""
        res = client.get("/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("MOD-06 Engine Prioritasi & Scoring Penanganan AI", data["modules_active"])
        print("✅ Health Check & Registrasi MOD-06: OK")

    def test_02_scoring_algorithm_unit(self):
        """Memvalidasi formula matematis 40% Keparahan, 30% Frekuensi, 30% Dampak"""
        sample_reports = [
            {
                "id_laporan": "TEST-REP-01",
                "nomor_tiket": "#TK-9901",
                "kategori": "AC",
                "lokasi": "Lab Komputer 3 – Gedung C",
                "tingkat_keparahan": "Berat",
                "kode_qr": "AC-L003-02",
                "status": "Diajukan",
                "created_at": "2026-11-09T08:00:00Z"
            },
            {
                "id_laporan": "TEST-REP-01B",
                "nomor_tiket": "#TK-9901B",
                "kategori": "AC",
                "lokasi": "Lab Komputer 3 – Gedung C",
                "tingkat_keparahan": "Berat",
                "kode_qr": "AC-L003-02",
                "status": "Diajukan",
                "created_at": "2026-11-09T08:30:00Z"
            },
            {
                "id_laporan": "TEST-REP-02",
                "nomor_tiket": "#TK-9902",
                "kategori": "Kursi",
                "lokasi": "Ruang A001 – Gedung A",
                "tingkat_keparahan": "Ringan",
                "kode_qr": "KR-TEST-01",
                "status": "Diajukan",
                "created_at": "2026-11-09T09:00:00Z"
            }
        ]

        scored = gemini_analytics.calculate_ticket_priorities(sample_reports)
        self.assertEqual(len(scored), 3)

        # Cek tiket 1 (AC di Lab dengan laporan berulang & keparahan Berat) -> Prioritas Tinggi (> 80)
        t1 = next(t for t in scored if t["id_laporan"] == "TEST-REP-01")
        self.assertGreater(t1["skor_urgensi"], 80)
        self.assertEqual(t1["kategori_prioritas"], "Tinggi")
        self.assertEqual(t1["breakdown"]["keparahan_nilai"], 100.0)
        self.assertEqual(t1["breakdown"]["keparahan_subskor"], 40.0)
        self.assertEqual(t1["breakdown"]["dampak_nilai"], 100.0) # 95 + 10 Lab bonus capped at 100
        self.assertEqual(t1["breakdown"]["dampak_subskor"], 30.0)
        self.assertGreaterEqual(t1["breakdown"]["frekuensi_count"], 2)

        # Cek tiket 2 (Kursi dengan keparahan Ringan) -> Prioritas Sedang atau Rendah (< 80)
        t2 = next(t for t in scored if t["id_laporan"] == "TEST-REP-02")
        self.assertLess(t2["skor_urgensi"], 80)
        self.assertIn(t2["kategori_prioritas"], ["Sedang", "Rendah"])
        print(f"✅ Formula Pembobotan Matematis & Thresholds (T1: {t1['skor_urgensi']} pts, T2: {t2['skor_urgensi']} pts): OK")

    def test_03_prioritize_tickets_endpoint_post(self):
        """Memvalidasi endpoint POST /api/v1/ai/prioritize-tickets"""
        res = client.post("/api/v1/ai/prioritize-tickets", json={"status_filter": "Semua"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("summary", data)
        self.assertIn("tickets", data)
        self.assertGreater(data["summary"]["total_evaluated"], 0)

        tickets = data["tickets"]
        # Pastikan terurut dari ranking #1 dengan skor tertinggi
        for i in range(len(tickets) - 1):
            self.assertGreaterEqual(tickets[i]["skor_urgensi"], tickets[i+1]["skor_urgensi"])
            self.assertEqual(tickets[i]["rank"], i + 1)

        print(f"✅ POST /api/v1/ai/prioritize-tickets ({data['summary']['total_evaluated']} tiket, Avg: {data['summary']['average_score']}): OK")

    def test_04_prioritized_tickets_endpoint_get_with_filter(self):
        """Memvalidasi endpoint GET /api/v1/ai/prioritized-tickets dengan query filter"""
        # Test Filter Prioritas Tinggi
        res = client.get("/api/v1/ai/prioritized-tickets?kategori_prioritas=Tinggi")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        for t in data["tickets"]:
            self.assertEqual(t["kategori_prioritas"], "Tinggi")
            self.assertGreater(t["skor_urgensi"], 80)
        print(f"✅ Filter Kategori Prioritas 'Tinggi' ({len(data['tickets'])} tiket ditemukan): OK")

        # Test Filter Prioritas Sedang
        res_sedang = client.get("/api/v1/ai/prioritized-tickets?kategori_prioritas=Sedang")
        self.assertEqual(res_sedang.status_code, 200)
        data_sedang = res_sedang.json()
        for t in data_sedang["tickets"]:
            self.assertEqual(t["kategori_prioritas"], "Sedang")
            self.assertTrue(50 <= t["skor_urgensi"] <= 80)
        print(f"✅ Filter Kategori Prioritas 'Sedang' ({len(data_sedang['tickets'])} tiket ditemukan): OK")

    def test_05_ticket_priority_detail(self):
        """Memvalidasi endpoint GET /api/v1/ai/prioritize-ticket/{id_laporan}"""
        all_reports = db.get_reports()
        self.assertGreater(len(all_reports), 0)
        sample_rep = all_reports[0]

        res = client.get(f"/api/v1/ai/prioritize-ticket/{sample_rep['id_laporan']}")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["id_laporan"], sample_rep["id_laporan"])
        self.assertIn("breakdown", data)
        self.assertIn("skor_urgensi", data)
        self.assertIn("rekomendasi_tindakan", data)
        print(f"✅ GET /api/v1/ai/prioritize-ticket/{sample_rep['id_laporan']} (Skor: {data['skor_urgensi']}): OK")

        # Uji tiket tidak ditemukan (HTTP 404)
        res_404 = client.get("/api/v1/ai/prioritize-ticket/LAP-NONEXISTENT")
        self.assertEqual(res_404.status_code, 404)
        print("✅ Skenario Tiket Tidak Ditemukan (HTTP 404): OK")

    def test_06_database_persistence_analisis_ai(self):
        """Memastikan entri kalkulasi prioritas tersimpan di koleksi ANALISIS_AI database JSON"""
        analyses = db.get_ai_analyses()
        prio_entries = [a for a in analyses if a.get("jenis") == "PRIORITAS_SKOR"]
        self.assertGreater(len(prio_entries), 0)
        latest = prio_entries[-1]
        self.assertIn("total_tiket_dievaluasi", latest)
        self.assertIn("top_urgent_ticket", latest)
        print(f"✅ Verifikasi Persistensi Entitas ANALISIS_AI (ID: {latest['id_analisis']}, Top Urgent: {latest['top_urgent_ticket']}): OK")

if __name__ == "__main__":
    unittest.main()
