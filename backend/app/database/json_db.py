import json
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from app.core.config import DB_FILE_PATH
from app.core.security import get_password_hash

_lock = threading.Lock()

DEFAULT_DATABASE_STRUCTURE: Dict[str, List[Dict[str, Any]]] = {
    "PENGGUNA": [],
    "DETAIL_AKUN": [],
    "FASILITAS": [
        {
            "id_fasilitas": "FAS-001",
            "kode_qr": "KR-A002-07",
            "nama_fasilitas": "Kursi Kuliah Ergonomis",
            "lokasi_gedung": "Ruang A002 – Gedung A",
            "kategori": "Kursi",
            "kondisi_terakhir": "Normal",
            "created_at": "2026-10-01T08:00:00Z"
        },
        {
            "id_fasilitas": "FAS-002",
            "kode_qr": "PJ-B101-01",
            "nama_fasilitas": "Proyektor Ruang B101",
            "lokasi_gedung": "Ruang B101 – Gedung B",
            "kategori": "Proyektor",
            "kondisi_terakhir": "Normal",
            "created_at": "2026-10-01T08:00:00Z"
        },
        {
            "id_fasilitas": "FAS-003",
            "kode_qr": "AC-L003-02",
            "nama_fasilitas": "Air Conditioner 2 PK",
            "lokasi_gedung": "Lab 3 – Gedung C",
            "kategori": "AC",
            "kondisi_terakhir": "Normal",
            "created_at": "2026-10-01T08:00:00Z"
        },
        {
            "id_fasilitas": "FAS-004",
            "kode_qr": "MJ-A001-03",
            "nama_fasilitas": "Meja Dosen & Mahasiswa",
            "lokasi_gedung": "Ruang A001 – Gedung A",
            "kategori": "Meja",
            "kondisi_terakhir": "Normal",
            "created_at": "2026-10-01T08:00:00Z"
        },
        {
            "id_fasilitas": "FAS-005",
            "kode_qr": "LP-C204-05",
            "nama_fasilitas": "Lampu LED Plafon",
            "lokasi_gedung": "Ruang C204 – Gedung C",
            "kategori": "Lampu",
            "kondisi_terakhir": "Normal",
            "created_at": "2026-10-01T08:00:00Z"
        }
    ],
    "LAPORAN": [],
    "STATUS_TIKET": [],
    "TINDAKAN_PENANGANAN": [],
    "ANALISIS_AI": []
}

class JsonDatabase:
    def __init__(self, file_path: Path = DB_FILE_PATH):
        self.file_path = file_path
        self._init_db()

    def _init_db(self):
        with _lock:
            if not self.file_path.exists():
                data = DEFAULT_DATABASE_STRUCTURE.copy()
                # Seed user awal: Mahasiswa Andrean & Admin
                default_password_hash = get_password_hash("password123")
                user_mhs = {
                    "id_user": "USR-001",
                    "nama": "Andrean",
                    "email": "andrean@kampus.ac.id",
                    "password": default_password_hash,
                    "role": "Mahasiswa",
                    "nomor_induk": "12345678",
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
                detail_mhs = {
                    "id_detail": "DET-001",
                    "id_user": "USR-001",
                    "fakultas": "Ilmu Komputer",
                    "prodi": "Teknik Informatika",
                    "telepon": "081234567890",
                    "foto_profil": "",
                    "status_aktif": True,
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
                user_admin = {
                    "id_user": "USR-002",
                    "nama": "Administrator Fasilitas",
                    "email": "admin@kampus.ac.id",
                    "password": default_password_hash,
                    "role": "Admin",
                    "nomor_induk": "19850101",
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
                detail_admin = {
                    "id_detail": "DET-002",
                    "id_user": "USR-002",
                    "fakultas": "Biro Fasilitas & Logistik",
                    "prodi": "Administrasi Fasilitas Kampus",
                    "telepon": "081298765432",
                    "foto_profil": "",
                    "status_aktif": True,
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
                data["PENGGUNA"].extend([user_mhs, user_admin])
                data["DETAIL_AKUN"].extend([detail_mhs, detail_admin])

                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

    def load_data(self) -> Dict[str, Any]:
        with _lock:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)

    def save_data(self, data: Dict[str, Any]):
        with _lock:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    # Helper Pengguna
    def get_users(self) -> List[Dict[str, Any]]:
        return self.load_data().get("PENGGUNA", [])

    def find_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        for user in self.get_users():
            if user.get("email", "").lower() == email.lower():
                return user
        return None

    def find_user_by_nomor_induk(self, nomor_induk: str) -> Optional[Dict[str, Any]]:
        for user in self.get_users():
            if user.get("nomor_induk") == nomor_induk:
                return user
        return None

    def find_user_by_id(self, id_user: str) -> Optional[Dict[str, Any]]:
        for user in self.get_users():
            if user.get("id_user") == id_user:
                return user
        return None

    def add_user(self, user_dict: Dict[str, Any], detail_dict: Optional[Dict[str, Any]] = None):
        data = self.load_data()
        data["PENGGUNA"].append(user_dict)
        if detail_dict:
            data["DETAIL_AKUN"].append(detail_dict)
        self.save_data(data)

    # Helper Fasilitas
    def get_facilities(self) -> List[Dict[str, Any]]:
        return self.load_data().get("FASILITAS", [])

    def find_facility_by_qr(self, kode_qr: str) -> Optional[Dict[str, Any]]:
        for fas in self.get_facilities():
            if fas.get("kode_qr", "").strip().upper() == kode_qr.strip().upper():
                return fas
        return None

    # Helper Laporan
    def get_reports(self) -> List[Dict[str, Any]]:
        return self.load_data().get("LAPORAN", [])

    def add_report(self, report_dict: Dict[str, Any]):
        data = self.load_data()
        data["LAPORAN"].append(report_dict)
        # Catat juga di STATUS_TIKET
        status_entry = {
            "id_status": f"STS-{len(data.get('STATUS_TIKET', [])) + 1:04d}",
            "id_laporan": report_dict.get("id_laporan"),
            "status": report_dict.get("status", "Diajukan"),
            "catatan": "Laporan berhasil diajukan ke sistem fasilitas kampus.",
            "updated_by": report_dict.get("id_user"),
            "timestamp": report_dict.get("created_at")
        }
        data["STATUS_TIKET"].append(status_entry)
        self.save_data(data)

db = JsonDatabase()
