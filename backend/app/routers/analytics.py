import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from app.models.analytics import (
    AnalyticsFilterRequest,
    ExecutiveSummaryResponse,
    AnalyticsHistoryItem
)
from app.database.json_db import db
from app.core.gemini_service import gemini_analytics

router = APIRouter(prefix="/api/v1/analytics", tags=["Subsistem Rangkuman Eksekutif AI"])

@router.post("/summary", response_model=ExecutiveSummaryResponse)
def generate_ai_executive_summary(filter_req: AnalyticsFilterRequest):
    """
    MOD-05: AI Summarization Pipeline & Ekstraksi Pola Kerusakan Dominan
    - Mengambil dataset laporan JSON sesuai filter (periode, gedung, kategori)
    - Google Gemini AI mensintesis ringkasan eksekutif dan rekomendasi perbaikan strategis
    - Menyimpan riwayat analisis ke entitas ANALISIS_AI
    """
    filtered_reports = db.filter_reports_for_analytics(
        periode=filter_req.periode,
        gedung=filter_req.gedung,
        kategori=filter_req.kategori
    )

    filter_label = f"{filter_req.periode} · {filter_req.gedung} · {filter_req.kategori}"

    # Jika filter tidak menemukan laporan sama sekali (Slide 26 Mockup: Data Tidak Ditemukan)
    if not filtered_reports:
        return ExecutiveSummaryResponse(
            found=False,
            id_analisis=None,
            filter_label=filter_label,
            total_laporan=0,
            bullets=[
                "Tidak ada data laporan kerusakan yang ditemukan untuk kriteria filter ini.",
                "Silakan periksa kembali pemilihan periode bulan, gedung, atau kategori fasilitas.",
                "Gunakan opsi 'Semua Gedung' atau 'Semua Kategori' untuk cakupan data yang lebih luas."
            ],
            rekomendasi="Ubah atau atur ulang filter pencarian untuk menampilkan data laporan lain.",
            statistik={
                "top_kategori": "-",
                "top_kategori_count": 0,
                "top_kategori_pct": 0,
                "top_gedung": "-",
                "top_gedung_count": 0,
                "tiket_kritis_menunggu": 0
            },
            created_at=datetime.now(timezone.utc).isoformat()
        )

    # Jalankan Pipeline Sintesis AI Gemini
    ai_result = gemini_analytics.synthesize_executive_summary(
        filtered_reports,
        {
            "periode": filter_req.periode,
            "gedung": filter_req.gedung,
            "kategori": filter_req.kategori
        }
    )

    new_id_analisis = f"ANL-{uuid.uuid4().hex[:8].upper()}"
    now_iso = datetime.now(timezone.utc).isoformat()

    # Catat ke entitas database ANALISIS_AI (Sesuai Spesifikasi MOD-05)
    analisis_entry = {
        "id_analisis": new_id_analisis,
        "tipe_analisis": "Rangkuman Eksekutif AI",
        "filter_applied": {
            "periode": filter_req.periode,
            "gedung": filter_req.gedung,
            "kategori": filter_req.kategori
        },
        "total_laporan_dianalisis": len(filtered_reports),
        "bullets": ai_result["bullets"],
        "rekomendasi": ai_result["rekomendasi"],
        "statistik": ai_result["statistik"],
        "created_at": now_iso
    }
    db.record_ai_analysis(analisis_entry)

    return ExecutiveSummaryResponse(
        found=True,
        id_analisis=new_id_analisis,
        filter_label=filter_label,
        total_laporan=len(filtered_reports),
        bullets=ai_result["bullets"],
        rekomendasi=ai_result["rekomendasi"],
        statistik=ai_result["statistik"],
        created_at=now_iso
    )

@router.get("/history", response_model=List[AnalyticsHistoryItem])
def get_analytics_history():
    """
    Mengambil riwayat seluruh rangkuman eksekutif AI yang telah digenerate
    """
    records = db.get_ai_analyses()
    return [
        AnalyticsHistoryItem(
            id_analisis=a["id_analisis"],
            tipe_analisis=a.get("tipe_analisis", "Rangkuman Eksekutif AI"),
            filter_applied=a.get("filter_applied", {}),
            total_laporan_dianalisis=a.get("total_laporan_dianalisis", 0),
            bullets=a.get("bullets", []),
            rekomendasi=a.get("rekomendasi", "-"),
            created_at=a.get("created_at", "")
        )
        for a in reversed(records)
    ]
