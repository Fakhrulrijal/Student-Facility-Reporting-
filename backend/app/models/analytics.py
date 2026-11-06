from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class AnalyticsFilterRequest(BaseModel):
    periode: str = "Oktober 2026"
    gedung: str = "Semua Gedung"
    kategori: str = "Semua Kategori"

class ExecutiveSummaryResponse(BaseModel):
    found: bool
    id_analisis: Optional[str] = None
    filter_label: str
    total_laporan: int
    bullets: List[str]
    rekomendasi: str
    statistik: Dict[str, Any]
    created_at: str

class AnalyticsHistoryItem(BaseModel):
    id_analisis: str
    tipe_analisis: str
    filter_applied: Dict[str, str]
    total_laporan_dianalisis: int
    bullets: List[str]
    rekomendasi: str
    created_at: str
