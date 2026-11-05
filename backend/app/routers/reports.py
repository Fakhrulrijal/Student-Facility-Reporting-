import os
import uuid
import shutil
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import UPLOAD_DIR
from app.core.security import decode_access_token
from app.database.json_db import db
from app.models.report import (
    LaporanCreateResponse,
    LaporanDetailResponse,
    LaporanHistoryResponse,
    TimelineStageItem,
    StatusTiketLog,
    UpdateStatusRequest
)

router = APIRouter(prefix="/api/v1/laporan", tags=["Pelaporan Kerusakan Fasilitas"])
security = HTTPBearer(auto_error=False)

def get_optional_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[dict]:
    if not credentials:
        return None
    payload = decode_access_token(credentials.credentials)
    if payload:
        return db.find_user_by_id(payload.get("sub"))
    return None

@router.post("", response_model=LaporanCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    foto: UploadFile = File(..., description="Foto bukti kerusakan fasilitas"),
    lokasi: str = Form(..., description="Lokasi gedung dan ruangan kerusakan"),
    kategori: str = Form(..., description="Kategori fasilitas (Kursi, Meja, Proyektor, AC, Lampu, Lainnya)"),
    tingkat_keparahan: str = Form(..., description="Tingkat keparahan (Ringan, Sedang, Berat)"),
    deskripsi: str = Form(..., description="Deskripsi detail kerusakan"),
    kode_qr: Optional[str] = Form(None, description="Kode QR aset jika ada"),
    current_user: Optional[dict] = Depends(get_optional_user)
):
    # Validasi input
    if not lokasi.strip():
        raise HTTPException(status_code=400, detail="Lokasi fasilitas wajib diisi.")
    if not deskripsi.strip():
        raise HTTPException(status_code=400, detail="Deskripsi kerusakan wajib diisi.")

    # Simpan file foto ke UPLOAD_DIR
    file_ext = Path(foto.filename).suffix if foto.filename else ".jpg"
    if not file_ext:
        file_ext = ".jpg"
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(foto.file, buffer)

    foto_url = f"/uploads/{unique_filename}"

    # Cari id_fasilitas jika ada kode_qr
    id_fasilitas = None
    if kode_qr:
        fas = db.find_facility_by_qr(kode_qr)
        if fas:
            id_fasilitas = fas["id_fasilitas"]

    # Generate Nomor Tiket (#TK-0001, #TK-0012, dst)
    reports = db.get_reports()
    ticket_num = len(reports) + 12  # dimulai dari #TK-0012 sesuai mockup
    nomor_tiket = f"#TK-{ticket_num:04d}"
    new_id_laporan = f"LAP-{uuid.uuid4().hex[:8].upper()}"
    now_iso = datetime.now(timezone.utc).isoformat()

    user_id = current_user["id_user"] if current_user else "USR-001"
    user_name = current_user["nama"] if current_user else "Andrean"

    report_record = {
        "id_laporan": new_id_laporan,
        "nomor_tiket": nomor_tiket,
        "id_user": user_id,
        "nama_pelapor": user_name,
        "id_fasilitas": id_fasilitas,
        "kode_qr": kode_qr.strip() if kode_qr else None,
        "lokasi": lokasi.strip(),
        "kategori": kategori.strip(),
        "tingkat_keparahan": tingkat_keparahan.strip(),
        "deskripsi": deskripsi.strip(),
        "foto_url": foto_url,
        "status": "Diajukan",
        "created_at": now_iso
    }

    db.add_report(report_record)

    return LaporanCreateResponse(
        id_laporan=new_id_laporan,
        nomor_tiket=nomor_tiket,
        status="Diajukan",
        kategori=kategori.strip(),
        lokasi=lokasi.strip(),
        tingkat_keparahan=tingkat_keparahan.strip(),
        deskripsi=deskripsi.strip(),
        foto_url=foto_url,
        kode_qr=kode_qr.strip() if kode_qr else None,
        created_at=now_iso,
        message="Laporan tersimpan dan menunggu peninjauan admin fasilitas."
    )

@router.get("", response_model=List[LaporanDetailResponse])
def get_all_reports():
    reports = db.get_reports()
    return [
        LaporanDetailResponse(
            id_laporan=r["id_laporan"],
            nomor_tiket=r["nomor_tiket"],
            id_user=r.get("id_user", "USR-001"),
            nama_pelapor=r.get("nama_pelapor", "Mahasiswa"),
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
        for r in reversed(reports)
    ]

@router.get("/{id_laporan}", response_model=LaporanDetailResponse)
def get_report_detail(id_laporan: str):
    search_id = id_laporan.strip().lstrip("#")
    for r in db.get_reports():
        tiket_clean = r.get("nomor_tiket", "").lstrip("#")
        if r["id_laporan"] == id_laporan or tiket_clean == search_id or r.get("nomor_tiket") == id_laporan:
            return LaporanDetailResponse(
                id_laporan=r["id_laporan"],
                nomor_tiket=r["nomor_tiket"],
                id_user=r.get("id_user", "USR-001"),
                nama_pelapor=r.get("nama_pelapor", "Mahasiswa"),
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
    raise HTTPException(status_code=404, detail="Laporan tidak ditemukan.")

@router.get("/user/{id_user}", response_model=List[LaporanDetailResponse])
def get_user_reports(id_user: str, status_filter: Optional[str] = None):
    """
    MOD-03: Tracking Status - Menampilkan daftar tiket laporan pengguna dengan filter status
    """
    reports = db.get_reports_by_user(id_user)
    
    if status_filter and status_filter.lower() != "semua":
        reports = [r for r in reports if r.get("status", "").lower() == status_filter.lower()]

    return [
        LaporanDetailResponse(
            id_laporan=r["id_laporan"],
            nomor_tiket=r["nomor_tiket"],
            id_user=r.get("id_user", id_user),
            nama_pelapor=r.get("nama_pelapor", "Mahasiswa"),
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
        for r in reversed(reports)
    ]

@router.get("/{id_laporan}/history", response_model=LaporanHistoryResponse)
def get_report_history(id_laporan: str):
    """
    MOD-03: Menampilkan rincian histori timeline vertikal status tiket
    (Diajukan -> Ditinjau Admin -> Diproses -> Selesai)
    """
    clean_id = id_laporan.strip().lstrip("#")
    matched_report = None
    for r in db.get_reports():
        if r["id_laporan"] == id_laporan or r.get("nomor_tiket", "").lstrip("#") == clean_id or r.get("nomor_tiket") == id_laporan:
            matched_report = r
            break

    if not matched_report:
        raise HTTPException(status_code=404, detail=f"Laporan '{id_laporan}' tidak ditemukan.")

    raw_history = db.get_history_by_report(matched_report["id_laporan"])
    current_status = matched_report.get("status", "Diajukan")

    # Mapping status logs
    log_map = {}
    for h in raw_history:
        log_map[h.get("status")] = h

    # 4 Tahap Timeline Standar Kampus (Slide 16 Mockup)
    stages_order = ["Diajukan", "Ditinjau Admin", "Diproses", "Selesai"]
    status_weights = {
        "Diajukan": 1,
        "Ditinjau Admin": 2,
        "Ditinjau": 2,
        "Diproses": 3,
        "Selesai": 4,
        "Ditolak": -1
    }
    current_weight = status_weights.get(current_status, 1)

    timeline_items = []
    for stage in stages_order:
        stage_weight = status_weights.get(stage, 0)
        is_completed = current_weight >= stage_weight
        is_current = (current_status == stage) or (stage == "Ditinjau Admin" and current_status == "Ditinjau")

        log = log_map.get(stage)
        timestamp = log.get("timestamp") if log else None
        catatan = log.get("catatan") if log else None
        petugas = log.get("updated_by") if log else None

        if not timestamp:
            if stage == "Ditinjau Admin" and current_weight < 2:
                catatan = "Menunggu peninjauan admin fasilitas"
            elif stage == "Diproses" and current_weight < 3:
                catatan = "–"
            elif stage == "Selesai" and current_weight < 4:
                catatan = "–"

        timeline_items.append(
            TimelineStageItem(
                stage_key=stage.lower().replace(" ", "_"),
                stage_name=stage,
                is_completed=is_completed,
                is_current=is_current,
                timestamp=timestamp,
                catatan=catatan,
                petugas=petugas
            )
        )

    return LaporanHistoryResponse(
        id_laporan=matched_report["id_laporan"],
        nomor_tiket=matched_report["nomor_tiket"],
        status_saat_ini=current_status,
        timeline=timeline_items,
        logs=[
            StatusTiketLog(
                id_status=h.get("id_status", ""),
                id_laporan=h.get("id_laporan", ""),
                status=h.get("status", ""),
                catatan=h.get("catatan", ""),
                updated_by=h.get("updated_by"),
                timestamp=h.get("timestamp", "")
            )
            for h in raw_history
        ]
    )

@router.put("/{id_laporan}/status", response_model=LaporanDetailResponse)
def update_report_status_endpoint(id_laporan: str, payload: UpdateStatusRequest):
    """
    Memperbarui status tiket perbaikan & menambahkan catatan teknis petugas
    """
    updated = db.update_report_status(
        id_laporan=id_laporan,
        new_status=payload.status,
        catatan=payload.catatan or "",
        updated_by=payload.updated_by or "Admin Fasilitas"
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Laporan tidak ditemukan.")

    return LaporanDetailResponse(
        id_laporan=updated["id_laporan"],
        nomor_tiket=updated["nomor_tiket"],
        id_user=updated.get("id_user", "USR-001"),
        nama_pelapor=updated.get("nama_pelapor", "Mahasiswa"),
        id_fasilitas=updated.get("id_fasilitas"),
        kode_qr=updated.get("kode_qr"),
        lokasi=updated["lokasi"],
        kategori=updated["kategori"],
        tingkat_keparahan=updated["tingkat_keparahan"],
        deskripsi=updated["deskripsi"],
        foto_url=updated["foto_url"],
        status=updated["status"],
        created_at=updated["created_at"]
    )
