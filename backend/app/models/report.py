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

class TimelineStageItem(BaseModel):
    stage_key: str  # "diajukan", "ditinjau", "diproses", "selesai"
    stage_name: str
    is_completed: bool
    is_current: bool
    timestamp: Optional[str] = None
    catatan: Optional[str] = None
    petugas: Optional[str] = None

class StatusTiketLog(BaseModel):
    id_status: str
    id_laporan: str
    status: str
    catatan: str
    updated_by: Optional[str] = None
    timestamp: str

class LaporanHistoryResponse(BaseModel):
    id_laporan: str
    nomor_tiket: str
    status_saat_ini: str
    timeline: List[TimelineStageItem]
    logs: List[StatusTiketLog]

class UpdateStatusRequest(BaseModel):
    status: str
    catatan: Optional[str] = None
    updated_by: Optional[str] = "Admin Fasilitas"

# MOD-04: Dashboard Admin & Kelola Tiket
class AdminDashboardSummaryResponse(BaseModel):
    total_laporan: int
    menunggu_peninjauan: int
    diproses: int
    selesai: int
    ditolak: int
    breakdown_kategori: dict

class AdminUpdateStatusRequest(BaseModel):
    status: str  # "Diproses", "Selesai", "Ditolak"
    aksi_teknis: Optional[str] = None  # "Perbaiki", "Ganti Baru"
    catatan: Optional[str] = None
    alasan_penolakan: Optional[str] = None
    admin_id: Optional[str] = "USR-002"
    admin_name: Optional[str] = "Administrator Fasilitas"

class FcmNotificationReceipt(BaseModel):
    success: bool
    message_id: str
    recipient_user_id: str
    title: str
    body: str
    timestamp: str

class AdminUpdateStatusResponse(BaseModel):
    id_laporan: str
    nomor_tiket: str
    status_baru: str
    aksi_teknis: Optional[str] = None
    catatan: Optional[str] = None
    alasan_penolakan: Optional[str] = None
    notification: FcmNotificationReceipt
    message: str = "Perubahan tersimpan di database dan notifikasi terkirim ke pelapor."

class AdminReportListResponse(BaseModel):
    total_laporan: int
    menunggu_peninjauan: int
    laporan: List[LaporanDetailResponse]
