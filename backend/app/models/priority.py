from pydantic import BaseModel, Field
from typing import List, Optional

class ScoreBreakdown(BaseModel):
    keparahan_nilai: float = Field(..., description="Nilai mentah keparahan (0-100)")
    keparahan_bobot: float = Field(0.40, description="Bobot variabel keparahan (40%)")
    keparahan_subskor: float = Field(..., description="Hasil keparahan * 0.40")
    
    frekuensi_nilai: float = Field(..., description="Nilai mentah frekuensi kerusakan (0-100)")
    frekuensi_bobot: float = Field(0.30, description="Bobot variabel frekuensi (30%)")
    frekuensi_subskor: float = Field(..., description="Hasil frekuensi * 0.30")
    frekuensi_count: int = Field(..., description="Jumlah laporan pada aset/gedung terkait")
    
    dampak_nilai: float = Field(..., description="Nilai mentah dampak fasilitas (0-100)")
    dampak_bobot: float = Field(0.30, description="Bobot variabel dampak fasilitas (30%)")
    dampak_subskor: float = Field(..., description="Hasil dampak * 0.30")
    dampak_keterangan: str = Field(..., description="Justifikasi dampak fasilitas terhadap kampus")

class PrioritizedTicket(BaseModel):
    rank: int = Field(..., description="Urutan prioritas penanganan (Rank #1, #2, dst.)")
    id_laporan: str
    nomor_tiket: str
    id_user: Optional[str] = None
    nama_pelapor: Optional[str] = None
    nomor_induk_pelapor: Optional[str] = None
    kategori: str
    lokasi: str
    tingkat_keparahan: str
    status: str
    foto_url: str
    kode_qr: Optional[str] = None
    skor_urgensi: int = Field(..., description="Skor Urgensi komposit akhir (0-100)")
    kategori_prioritas: str = Field(..., description="Klasifikasi: Tinggi (>80), Sedang (50-80), Rendah (<50)")
    rekomendasi_tindakan: str = Field(..., description="Rekomendasi penanganan teknis")
    breakdown: ScoreBreakdown
    created_at: str

class PrioritizeSummary(BaseModel):
    total_evaluated: int
    total_tinggi: int
    total_sedang: int
    total_rendah: int
    average_score: float

class PrioritizeResponse(BaseModel):
    status: str = "success"
    message: str
    summary: PrioritizeSummary
    tickets: List[PrioritizedTicket]
    timestamp: str

class PrioritizeFilterRequest(BaseModel):
    status_filter: Optional[str] = "Semua" # Semua, Diajukan, Diproses, Selesai
    kategori_prioritas: Optional[str] = "Semua" # Semua, Tinggi, Sedang, Rendah
    gedung: Optional[str] = "Semua Gedung"
