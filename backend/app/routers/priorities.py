from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from datetime import datetime, timezone

from app.database.json_db import db
from app.core.gemini_service import gemini_analytics
from app.models.priority import (
    PrioritizeResponse,
    PrioritizedTicket,
    PrioritizeSummary,
    PrioritizeFilterRequest,
)

router = APIRouter(prefix="/api/v1/ai", tags=["MOD-06: Prioritasi & Scoring AI"])

@router.post("/prioritize-tickets", response_model=PrioritizeResponse)
def prioritize_tickets(payload: Optional[PrioritizeFilterRequest] = None):
    """
    MOD-06: Mengkalkulasi Skor Urgensi (0-100) dan perangkingan tiket fasilitas secara otomatis
    berbasis formula komposit Google Gemini AI & Heuristik:
    - Keparahan Laporan (Weight 40%)
    - Frekuensi Pelaporan Aset/Gedung Sama (Weight 30%)
    - Dampak Fasilitas terhadap Kegiatan Kampus (Weight 30%)
    """
    all_reports = db.get_reports()
    if not all_reports:
        return PrioritizeResponse(
            status="success",
            message="Belum ada laporan kerusakan yang tercatat di sistem.",
            summary=PrioritizeSummary(
                total_evaluated=0,
                total_tinggi=0,
                total_sedang=0,
                total_rendah=0,
                average_score=0.0
            ),
            tickets=[],
            timestamp=datetime.now(timezone.utc).isoformat()
        )

    # Lakukan kalkulasi scoring komposit
    prioritized_list = gemini_analytics.calculate_ticket_priorities(all_reports)

    # Simpan hasil analisis & sinkronisasi entitas database
    db.save_prioritization_results(prioritized_list)

    # Filter hasil jika diminta
    status_filter = payload.status_filter if payload else "Semua"
    kategori_prio = payload.kategori_prioritas if payload else "Semua"
    gedung_filter = payload.gedung if payload else "Semua Gedung"

    filtered_tickets = []
    for item in prioritized_list:
        # Filter Status (misal: hanya yang aktif / Diajukan / Diproses)
        if status_filter and status_filter != "Semua":
            if item.get("status") != status_filter:
                continue

        # Filter Kategori Prioritas (Tinggi, Sedang, Rendah)
        if kategori_prio and kategori_prio != "Semua":
            if item.get("kategori_prioritas") != kategori_prio:
                continue

        # Filter Gedung
        if gedung_filter and gedung_filter != "Semua Gedung" and gedung_filter != "Semua":
            if gedung_filter.lower() not in item.get("lokasi", "").lower():
                continue

        filtered_tickets.append(item)

    # Hitung metrik ringkasan
    total_eval = len(filtered_tickets)
    total_tinggi = sum(1 for t in filtered_tickets if t.get("kategori_prioritas") == "Tinggi")
    total_sedang = sum(1 for t in filtered_tickets if t.get("kategori_prioritas") == "Sedang")
    total_rendah = sum(1 for t in filtered_tickets if t.get("kategori_prioritas") == "Rendah")
    avg_score = round(sum(t.get("skor_urgensi", 0) for t in filtered_tickets) / total_eval, 1) if total_eval > 0 else 0.0

    return PrioritizeResponse(
        status="success",
        message=f"Berhasil mengkalkulasi prioritas untuk {total_eval} laporan fasilitas.",
        summary=PrioritizeSummary(
            total_evaluated=total_eval,
            total_tinggi=total_tinggi,
            total_sedang=total_sedang,
            total_rendah=total_rendah,
            average_score=avg_score
        ),
        tickets=filtered_tickets,
        timestamp=datetime.now(timezone.utc).isoformat()
    )

@router.get("/prioritized-tickets", response_model=PrioritizeResponse)
def get_prioritized_tickets(
    status_filter: str = Query("Semua", description="Filter status tiket (Semua, Diajukan, Diproses, Selesai)"),
    kategori_prioritas: str = Query("Semua", description="Filter prioritas (Semua, Tinggi, Sedang, Rendah)"),
    gedung: str = Query("Semua Gedung", description="Filter gedung spesifik")
):
    """
    MOD-06: Mengambil daftar tiket yang telah diperingkatkan berdasarkan skor urgensi.
    """
    filter_req = PrioritizeFilterRequest(
        status_filter=status_filter,
        kategori_prioritas=kategori_prioritas,
        gedung=gedung
    )
    return prioritize_tickets(filter_req)

@router.get("/prioritize-ticket/{id_laporan}", response_model=PrioritizedTicket)
def get_ticket_priority_detail(id_laporan: str):
    """
    MOD-06: Mengambil rincian skor urgensi dan breakdown pembobotan untuk satu tiket spesifik.
    """
    clean_id = id_laporan.lstrip("#")
    all_reports = db.get_reports()
    
    # Cari target laporan
    target = None
    for r in all_reports:
        if r.get("id_laporan") == clean_id or r.get("nomor_tiket") == id_laporan or r.get("nomor_tiket") == f"#{clean_id}":
            target = r
            break

    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Laporan dengan id/nomor '{id_laporan}' tidak ditemukan."
        )

    # Evaluasi prioritas
    prioritized_list = gemini_analytics.calculate_ticket_priorities(all_reports)
    for p in prioritized_list:
        if p["id_laporan"] == target["id_laporan"]:
            return p

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Gagal mengevaluasi skor urgensi untuk laporan ini."
    )
