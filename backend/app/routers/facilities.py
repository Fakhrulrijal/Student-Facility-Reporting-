from typing import List
from fastapi import APIRouter, HTTPException, status
from app.models.report import FasilitasResponse
from app.database.json_db import db

router = APIRouter(prefix="/api/v1/fasilitas", tags=["Fasilitas & QR Asset"])

@router.get("", response_model=List[FasilitasResponse])
def get_all_facilities():
    facilities = db.get_facilities()
    return [
        FasilitasResponse(
            id_fasilitas=f["id_fasilitas"],
            kode_qr=f["kode_qr"],
            nama_fasilitas=f["nama_fasilitas"],
            lokasi_gedung=f["lokasi_gedung"],
            kategori=f["kategori"],
            kondisi_terakhir=f.get("kondisi_terakhir", "Normal")
        )
        for f in facilities
    ]

@router.get("/qr/{kode_qr}", response_model=FasilitasResponse)
def get_facility_by_qr(kode_qr: str):
    facility = db.find_facility_by_qr(kode_qr)
    if not facility:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Kode QR '{kode_qr}' tidak dikenali. Kode bukan milik fasilitas kampus atau rusak."
        )
    return FasilitasResponse(
        id_fasilitas=facility["id_fasilitas"],
        kode_qr=facility["kode_qr"],
        nama_fasilitas=facility["nama_fasilitas"],
        lokasi_gedung=facility["lokasi_gedung"],
        kategori=facility["kategori"],
        kondisi_terakhir=facility.get("kondisi_terakhir", "Normal")
    )
