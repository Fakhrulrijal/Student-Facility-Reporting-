from typing import Optional, List
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.report import (
    AdminDashboardSummaryResponse,
    AdminReportListResponse,
    AdminUpdateStatusRequest,
    AdminUpdateStatusResponse,
    LaporanDetailResponse,
    FcmNotificationReceipt
)
from app.database.json_db import db

router = APIRouter(prefix="/api/v1/admin", tags=["Admin Dashboard & Kelola Laporan"])

@router.get("/dashboard/summary", response_model=AdminDashboardSummaryResponse)
def get_dashboard_summary():
    """
    MOD-04: Ringkasan statistik dashboard admin
    (Total laporan, diproses, selesai, breakdown kategori kerusakan)
    """
    summary = db.get_admin_dashboard_summary()
    return AdminDashboardSummaryResponse(**summary)

@router.get("/laporan", response_model=AdminReportListResponse)
def get_admin_reports(status_filter: Optional[str] = None):
    """
    MOD-04: Manajemen seluruh tiket laporan untuk admin dengan filter status
    """
    all_reports = db.get_reports()
    menunggu_count = sum(1 for r in all_reports if r.get("status") == "Diajukan")

    filtered = all_reports
    if status_filter and status_filter.lower() != "semua":
        filtered = [r for r in all_reports if r.get("status", "").lower() == status_filter.lower()]

    report_items = [
        LaporanDetailResponse(
            id_laporan=r["id_laporan"],
            nomor_tiket=r["nomor_tiket"],
            id_user=r.get("id_user", "USR-001"),
            nama_pelapor=r.get("nama_pelapor", "Andrean"),
            nomor_induk_pelapor=r.get("nomor_induk_pelapor", "12345678"),
            id_fasilitas=r.get("id_fasilitas"),
            kode_qr=r.get("kode_qr"),
            lokasi=r["lokasi"],
            kategori=r["kategori"],
            tingkat_keparahan=r["tingkat_keparahan"],
            deskripsi=r["deskripsi"],
            foto_url=r["foto_url"],
            status=r.get("status", "Diajukan"),
            created_at=r["created_at"]
        )
        for r in reversed(filtered)
    ]

    return AdminReportListResponse(
        total_laporan=len(all_reports),
        menunggu_peninjauan=menunggu_count,
        laporan=report_items
    )

@router.put("/laporan/{id_laporan}/status", response_model=AdminUpdateStatusResponse)
def admin_update_report_status(id_laporan: str, payload: AdminUpdateStatusRequest):
    """
    MOD-04: Workflow Verifikasi Tiket Admin
    - Jika Layak: Aksi Teknis (Perbaiki / Ganti Baru) -> Status 'Diproses' atau 'Selesai'
    - Jika Tidak Layak: Wajib isi Alasan Penolakan -> Status 'Ditolak'
    - Simpan ke relasi TINDAKAN_PENANGANAN & trigger notifikasi Firebase (FCM) ke pelapor
    """
    if payload.status == "Ditolak" and (not payload.alasan_penolakan or not payload.alasan_penolakan.strip()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Alasan penolakan wajib diisi jika laporan dinyatakan tidak layak."
        )

    result = db.admin_process_report(
        id_laporan=id_laporan,
        new_status=payload.status,
        aksi_teknis=payload.aksi_teknis,
        catatan=payload.catatan,
        alasan_penolakan=payload.alasan_penolakan,
        admin_id=payload.admin_id or "USR-002",
        admin_name=payload.admin_name or "Administrator Fasilitas"
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Laporan '{id_laporan}' tidak ditemukan."
        )

    target = result["target_report"]
    notif = result["notification"]

    return AdminUpdateStatusResponse(
        id_laporan=target["id_laporan"],
        nomor_tiket=target["nomor_tiket"],
        status_baru=payload.status,
        aksi_teknis=payload.aksi_teknis,
        catatan=payload.catatan,
        alasan_penolakan=payload.alasan_penolakan,
        notification=FcmNotificationReceipt(**notif),
        message="Perubahan status tiket berhasil disimpan dan notifikasi telah dikirim ke perangkat pelapor."
    )
