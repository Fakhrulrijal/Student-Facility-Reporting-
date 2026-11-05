from enum import Enum
from typing import Optional, List
from pydantic import BaseModel

class TingkatKeparahan(str, Enum):
    RINGAN = "Ringan"
    SEDANG = "Sedang"
    BERAT = "Berat"

class KategoriFasilitas(str, Enum):
    KURSI = "Kursi"
    MEJA = "Meja"
    PROYEKTOR = "Proyektor"
    AC = "AC"
    LAMPU = "Lampu"
    LAINNYA = "Lainnya"

class FasilitasResponse(BaseModel):
    id_fasilitas: str
    kode_qr: str
    nama_fasilitas: str
    lokasi_gedung: str
    kategori: str
    kondisi_terakhir: Optional[str] = "Normal"

class LaporanCreateResponse(BaseModel):
    id_laporan: str
    nomor_tiket: str
    status: str
    kategori: str
    lokasi: str
    tingkat_keparahan: str
    deskripsi: str
    foto_url: str
    kode_qr: Optional[str] = None
    created_at: str
    message: str = "Laporan berhasil diajukan dan tiket baru telah diterbitkan."

class LaporanDetailResponse(BaseModel):
    id_laporan: str
    nomor_tiket: str
    id_user: str
    nama_pelapor: Optional[str] = None
    nomor_induk_pelapor: Optional[str] = None
    id_fasilitas: Optional[str] = None
    kode_qr: Optional[str] = None
    lokasi: str
    kategori: str
    tingkat_keparahan: str
    deskripsi: str
    foto_url: str
    status: str
    created_at: str
