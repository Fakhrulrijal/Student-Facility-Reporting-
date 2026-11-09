import json
import uuid
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

                # Seed sample laporan historis (Oktober 2026) sesuai Diagram 4 & 5 Mockup
                sample_reports = [
                    {
                        "id_laporan": "LAP-0012",
                        "nomor_tiket": "#TK-0012",
                        "id_user": "USR-001",
                        "nama_pelapor": "Andrean",
                        "nomor_induk_pelapor": "12345678",
                        "id_fasilitas": "FAS-001",
                        "kode_qr": "KR-A002-07",
                        "lokasi": "Ruang A002 – Gedung A",
                        "kategori": "Kursi",
                        "tingkat_keparahan": "Sedang",
                        "deskripsi": "Sandaran kursi patah saat dipakai, berbahaya untuk mahasiswa.",
                        "foto_url": "/uploads/sample_kursi.jpg",
                        "status": "Diajukan",
                        "created_at": "2026-10-29T10:15:00Z"
                    },
                    {
                        "id_laporan": "LAP-0010",
                        "nomor_tiket": "#TK-0010",
                        "id_user": "USR-001",
                        "nama_pelapor": "Siti",
                        "nomor_induk_pelapor": "12345679",
                        "id_fasilitas": "FAS-002",
                        "kode_qr": "PJ-B101-01",
                        "lokasi": "Ruang B101 – Gedung B",
                        "kategori": "Proyektor",
                        "tingkat_keparahan": "Sedang",
                        "deskripsi": "Proyektor berkedip dan mati otomatis setelah 10 menit.",
                        "foto_url": "/uploads/sample_proyektor.jpg",
                        "status": "Diproses",
                        "created_at": "2026-10-18T09:30:00Z"
                    },
                    {
                        "id_laporan": "LAP-0008",
                        "nomor_tiket": "#TK-0008",
                        "id_user": "USR-001",
                        "nama_pelapor": "Budi",
                        "nomor_induk_pelapor": "12345680",
                        "id_fasilitas": "FAS-005",
                        "kode_qr": "LP-C204-05",
                        "lokasi": "Ruang C204 – Gedung C",
                        "kategori": "Lampu / AC",
                        "tingkat_keparahan": "Ringan",
                        "deskripsi": "Lampu plafon redup dan mengeluarkan bunyi dengung.",
                        "foto_url": "/uploads/sample_lampu.jpg",
                        "status": "Selesai",
                        "created_at": "2026-10-02T14:00:00Z"
                    }
                ]
                data["LAPORAN"].extend(sample_reports)

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

    def get_reports_by_user(self, id_or_nim: str) -> List[Dict[str, Any]]:
        clean_id = id_or_nim.strip()
        matched_user_ids = {clean_id}
        # Cek apakah ini NIM
        user = self.find_user_by_nomor_induk(clean_id)
        if user:
            matched_user_ids.add(user["id_user"])
        # Cek jika id_user
        user_by_id = self.find_user_by_id(clean_id)
        if user_by_id:
            matched_user_ids.add(user_by_id["nomor_induk"])

        reports = self.get_reports()
        return [
            r for r in reports
            if r.get("id_user") in matched_user_ids or r.get("nomor_induk_pelapor") in matched_user_ids
        ]

    def get_history_by_report(self, id_laporan_or_ticket: str) -> List[Dict[str, Any]]:
        clean = id_laporan_or_ticket.strip().lstrip("#")
        # Cari id_laporan yang cocok
        target_id = None
        for r in self.get_reports():
            if r.get("id_laporan") == id_laporan_or_ticket or r.get("nomor_tiket", "").lstrip("#") == clean:
                target_id = r.get("id_laporan")
                break

        if not target_id:
            target_id = id_laporan_or_ticket

        all_status = self.load_data().get("STATUS_TIKET", [])
        return [s for s in all_status if s.get("id_laporan") == target_id]

    def update_report_status(self, id_laporan: str, new_status: str, catatan: str = "", updated_by: str = "Admin"):
        data = self.load_data()
        target_report = None
        clean = id_laporan.strip().lstrip("#")
        for r in data.get("LAPORAN", []):
            if r.get("id_laporan") == id_laporan or r.get("nomor_tiket", "").lstrip("#") == clean:
                r["status"] = new_status
                target_report = r
                break

        if target_report:
            now_iso = datetime.now(timezone.utc).isoformat()
            status_entry = {
                "id_status": f"STS-{len(data.get('STATUS_TIKET', [])) + 1:04d}",
                "id_laporan": target_report.get("id_laporan"),
                "status": new_status,
                "catatan": catatan or f"Status tiket diperbarui menjadi {new_status}.",
                "updated_by": updated_by,
                "timestamp": now_iso
            }
            data["STATUS_TIKET"].append(status_entry)
            self.save_data(data)
            return target_report
        return None

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

    # MOD-04: Helper Dashboard Admin & Verifikasi Tiket
    def get_admin_dashboard_summary(self) -> Dict[str, Any]:
        reports = self.get_reports()
        total = len(reports)
        diajukan = sum(1 for r in reports if r.get("status") == "Diajukan")
        diproses = sum(1 for r in reports if r.get("status") == "Diproses")
        selesai = sum(1 for r in reports if r.get("status") == "Selesai")
        ditolak = sum(1 for r in reports if r.get("status") == "Ditolak")

        # Breakdown kategori
        kategori_counts = {
            "Kursi": 0,
            "Proyektor": 0,
            "Lampu / AC": 0,
            "DLL": 0
        }
        for r in reports:
            kat = r.get("kategori", "").strip()
            if kat == "Kursi":
                kategori_counts["Kursi"] += 1
            elif kat == "Proyektor":
                kategori_counts["Proyektor"] += 1
            elif kat in ["Lampu", "AC", "Lampu / AC"]:
                kategori_counts["Lampu / AC"] += 1
            else:
                kategori_counts["DLL"] += 1

        return {
            "total_laporan": total,
            "menunggu_peninjauan": diajukan,
            "diproses": diproses,
            "selesai": selesai,
            "ditolak": ditolak,
            "breakdown_kategori": kategori_counts
        }

    def admin_process_report(
        self,
        id_laporan: str,
        new_status: str,
        aksi_teknis: Optional[str] = None,
        catatan: Optional[str] = None,
        alasan_penolakan: Optional[str] = None,
        admin_id: str = "USR-002",
        admin_name: str = "Administrator Fasilitas"
    ) -> Optional[Dict[str, Any]]:
        data = self.load_data()
        target_report = None
        clean = id_laporan.strip().lstrip("#")

        for r in data.get("LAPORAN", []):
            if r.get("id_laporan") == id_laporan or r.get("nomor_tiket", "").lstrip("#") == clean:
                r["status"] = new_status
                target_report = r
                break

        if not target_report:
            return None

        now_iso = datetime.now(timezone.utc).isoformat()

        # 1. Catat ke STATUS_TIKET
        final_catatan = catatan
        if new_status == "Ditolak":
            final_catatan = f"Laporan ditolak: {alasan_penolakan}"
        elif not final_catatan:
            final_catatan = f"Status tiket diperbarui menjadi {new_status} ({aksi_teknis or 'Pemeriksaan'})."

        status_entry = {
            "id_status": f"STS-{len(data.get('STATUS_TIKET', [])) + 1:04d}",
            "id_laporan": target_report.get("id_laporan"),
            "status": new_status,
            "catatan": final_catatan,
            "updated_by": admin_name,
            "timestamp": now_iso
        }
        data["STATUS_TIKET"].append(status_entry)

        # 2. Catat ke TINDAKAN_PENANGANAN (Relasi Database MOD-04)
        tindakan_entry = {
            "id_tindakan": f"TDK-{len(data.get('TINDAKAN_PENANGANAN', [])) + 1:04d}",
            "id_laporan": target_report.get("id_laporan"),
            "nomor_tiket": target_report.get("nomor_tiket"),
            "status_akhir": new_status,
            "aksi_teknis": aksi_teknis if new_status != "Ditolak" else "Penolakan",
            "alasan_penolakan": alasan_penolakan,
            "catatan_admin": catatan,
            "diproses_oleh": admin_id,
            "nama_admin": admin_name,
            "timestamp": now_iso
        }
        data["TINDAKAN_PENANGANAN"].append(tindakan_entry)

        self.save_data(data)

        # 3. Trigger Mock Firebase Cloud Messaging (FCM) Notification
        fcm_message_id = f"fcm_msg_{uuid.uuid4().hex[:12]}"
        notif_title = f"Update Tiket {target_report.get('nomor_tiket')}"
        if new_status == "Ditolak":
            notif_body = f"Laporan Anda ditolak. Alasan: {alasan_penolakan}"
        else:
            notif_body = f"Laporan Anda kini berstatus '{new_status}' dengan aksi '{aksi_teknis or 'Penanganan'}'. {catatan or ''}"

        return {
            "target_report": target_report,
            "tindakan": tindakan_entry,
            "notification": {
                "success": True,
                "message_id": fcm_message_id,
                "recipient_user_id": target_report.get("id_user", "USR-001"),
                "title": notif_title,
                "body": notif_body,
                "timestamp": now_iso
            }
        }

    # MOD-05: AI Analytics & Rangkuman Eksekutif
    def filter_reports_for_analytics(
        self,
        periode: str = "Semua",
        gedung: str = "Semua Gedung",
        kategori: str = "Semua Kategori"
    ) -> List[Dict[str, Any]]:
        reports = self.get_reports()
        filtered = []

        month_map = {
            "januari": "01", "jan": "01",
            "februari": "02", "feb": "02",
            "maret": "03", "mar": "03",
            "april": "04", "apr": "04",
            "mei": "05",
            "juni": "06", "jun": "06",
            "juli": "07", "jul": "07",
            "agustus": "08", "agu": "08", "agt": "08",
            "september": "09", "sep": "09",
            "oktober": "10", "okt": "10",
            "november": "11", "nov": "11",
            "desember": "12", "des": "12"
        }

        # Deteksi bulan/tahun dari string periode (misal: "Oktober 2026" atau "Okt 2026")
        target_year_month = None
        p_lower = periode.lower()
        if "semua" not in p_lower:
            for m_name, m_num in month_map.items():
                if m_name in p_lower:
                    import re
                    match = re.search(r"\b(20\d\d)\b", periode)
                    year = match.group(1) if match else "2026"
                    target_year_month = f"{year}-{m_num}"
                    break

        for r in reports:
            # Filter Kategori
            if kategori and kategori != "Semua Kategori" and kategori != "Semua":
                if r.get("kategori", "").lower() != kategori.lower():
                    continue

            # Filter Gedung (berdasarkan string di kolom lokasi)
            if gedung and gedung != "Semua Gedung" and gedung != "Semua":
                if gedung.lower() not in r.get("lokasi", "").lower():
                    continue

            # Filter Periode jika ada spesifik (abaikan jika 'Semua')
            if target_year_month:
                created_at = r.get("created_at", "")
                if not created_at.startswith(target_year_month):
                    continue

            filtered.append(r)

        return filtered

    def record_ai_analysis(self, analysis_entry: Dict[str, Any]):
        data = self.load_data()
        data["ANALISIS_AI"].append(analysis_entry)
        self.save_data(data)

    def get_ai_analyses(self) -> List[Dict[str, Any]]:
        return self.load_data().get("ANALISIS_AI", [])

    # MOD-06: Simpan & Perbarui Hasil Kalkulasi Prioritas AI
    def save_prioritization_results(self, prioritized_tickets: List[Dict[str, Any]]) -> Dict[str, Any]:
        data = self.load_data()
        now_iso = datetime.now(timezone.utc).isoformat()
        
        # Buat entri log analisis di ANALISIS_AI
        summary_entry = {
            "id_analisis": f"ANL-PRIO-{uuid.uuid4().hex[:8].upper()}",
            "jenis": "PRIORITAS_SKOR",
            "total_tiket_dievaluasi": len(prioritized_tickets),
            "total_tinggi": sum(1 for t in prioritized_tickets if t.get("kategori_prioritas") == "Tinggi"),
            "total_sedang": sum(1 for t in prioritized_tickets if t.get("kategori_prioritas") == "Sedang"),
            "total_rendah": sum(1 for t in prioritized_tickets if t.get("kategori_prioritas") == "Rendah"),
            "top_urgent_ticket": prioritized_tickets[0]["nomor_tiket"] if prioritized_tickets else None,
            "created_at": now_iso
        }
        data["ANALISIS_AI"].append(summary_entry)

        # Sinkronkan skor urgensi dan prioritas pada setiap laporan di LAPORAN
        ticket_map = {t["id_laporan"]: t for t in prioritized_tickets}
        for rep in data["LAPORAN"]:
            if rep["id_laporan"] in ticket_map:
                p_info = ticket_map[rep["id_laporan"]]
                rep["skor_urgensi"] = p_info["skor_urgensi"]
                rep["kategori_prioritas"] = p_info["kategori_prioritas"]
                rep["rank_prioritas"] = p_info["rank"]

        self.save_data(data)
        return summary_entry

db = JsonDatabase()
