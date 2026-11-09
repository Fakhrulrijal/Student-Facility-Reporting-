import os
import json
from typing import Dict, Any, List, Optional
from collections import Counter

class GeminiAnalyticsService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self._client = None
        if self.api_key:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except Exception:
                self._client = None

    def synthesize_executive_summary(
        self,
        reports: List[Dict[str, Any]],
        filter_info: Dict[str, str]
    ) -> Dict[str, Any]:
        total = len(reports)
        if total == 0:
            return {
                "found": False,
                "message": "Tidak ada laporan yang sesuai dengan filter yang dipilih."
            }

        # 1. Ekstraksi Metrik Dasar
        kat_counts = Counter(r.get("kategori", "Lainnya") for r in reports)
        top_kategori, top_kat_count = kat_counts.most_common(1)[0]
        top_kat_pct = round((top_kat_count / total) * 100)

        # Ekstraksi gedung dari teks lokasi
        gedung_list = []
        for r in reports:
            lok = r.get("lokasi", "")
            if "Gedung A" in lok:
                gedung_list.append("Gedung A")
            elif "Gedung B" in lok:
                gedung_list.append("Gedung B")
            elif "Gedung C" in lok:
                gedung_list.append("Gedung C")
            elif "Lab" in lok:
                gedung_list.append("Area Laboratorium")
            else:
                gedung_list.append("Area Kampus Umum")

        gedung_counts = Counter(gedung_list)
        top_gedung, top_gedung_count = gedung_counts.most_common(1)[0]

        # Laporan berkeparahan Berat / Tinggi yang masih Diajukan
        kritis_count = sum(
            1 for r in reports
            if r.get("tingkat_keparahan") in ["Berat", "Tinggi", "Sedang"] and r.get("status") == "Diajukan"
        )

        # Default fallback summary berbasis pola empiris (Slide 25 Mockup)
        bullet1 = f"{top_kategori} menjadi fasilitas paling sering rusak ({top_kat_count} laporan, {top_kat_pct}%)."
        bullet2 = f"{top_gedung} mencatat {top_gedung_count} laporan, mendominasi area fasilitas bermasalah."
        bullet3 = f"{kritis_count} laporan berkeparahan tinggi masih berstatus Diajukan."
        rekomendasi = f"Jadwalkan perbaikan {top_kategori.lower()} massal dan inspeksi menyeluruh di {top_gedung}."

        # 2. Jika Google Gemini Client tersedia, lakukan prompt summarization
        if self._client:
            try:
                prompt = f"""
Anda adalah AI Fasilitas Kampus. Analisislah data pelaporan kerusakan fasilitas kampus berikut ini dan berikan ringkasan eksekutif singkat:
- Filter: {filter_info}
- Total Laporan: {total}
- Kategori terbanyak: {top_kategori} ({top_kat_count} laporan, {top_kat_pct}%)
- Gedung terbanyak: {top_gedung} ({top_gedung_count} laporan)
- Laporan status Diajukan: {kritis_count}

Format respon wajib JSON dengan key:
- bullet_1: ringkasan pola fasilitas paling sering rusak
- bullet_2: tren gedung dengan laporan tertinggi
- bullet_3: status laporan yang mendesak
- rekomendasi: rekomendasi tindakan strategis untuk biro logistik/admin
"""
                response = self._client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                if response and response.text:
                    # Parse json jika ada
                    text = response.text.strip()
                    if "```json" in text:
                        text = text.split("```json")[1].split("```")[0].strip()
                    elif "```" in text:
                        text = text.split("```")[1].split("```")[0].strip()
                    data_json = json.loads(text)
                    bullet1 = data_json.get("bullet_1", bullet1)
                    bullet2 = data_json.get("bullet_2", bullet2)
                    bullet3 = data_json.get("bullet_3", bullet3)
                    rekomendasi = data_json.get("rekomendasi", rekomendasi)
            except Exception:
                pass  # Gunakan sintesis berbasis pola yang telah teruji

        return {
            "found": True,
            "filter_applied": filter_info,
            "total_laporan": total,
            "bullets": [bullet1, bullet2, bullet3],
            "rekomendasi": rekomendasi,
            "statistik": {
                "top_kategori": top_kategori,
                "top_kategori_count": top_kat_count,
                "top_kategori_pct": top_kat_pct,
                "top_gedung": top_gedung,
                "top_gedung_count": top_gedung_count,
                "tiket_kritis_menunggu": kritis_count,
            }
        }

    def calculate_ticket_priorities(self, reports: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        MOD-06: Mengkalkulasi skor urgensi 0-100 berbasis formula komposit:
        - Keparahan Laporan (Weight 40%)
        - Frekuensi Pelaporan Aset/Gedung Sama (Weight 30%)
        - Dampak Fasilitas terhadap Kegiatan Kampus (Weight 30%)
        """
        if not reports:
            return []

        # Hitung frekuensi per kode QR dan per lokasi
        qr_counter = Counter(r.get("kode_qr") for r in reports if r.get("kode_qr"))
        location_counter = Counter(r.get("lokasi", "").strip().lower() for r in reports if r.get("lokasi"))
        kategori_counter = Counter(r.get("kategori", "").strip().lower() for r in reports if r.get("kategori"))

        prioritized = []

        for r in reports:
            # 1. Keparahan Laporan (Weight 40%)
            kep_str = str(r.get("tingkat_keparahan", "Sedang")).strip().lower()
            if "berat" in kep_str or "tinggi" in kep_str:
                keparahan_nilai = 100.0
            elif "sedang" in kep_str:
                keparahan_nilai = 60.0
            else: # Ringan / Rendah
                keparahan_nilai = 30.0
            keparahan_subskor = round(keparahan_nilai * 0.40, 2)

            # 2. Frekuensi Kerusakan Aset / Gedung (Weight 30%)
            qr = r.get("kode_qr")
            lok = r.get("lokasi", "").strip().lower()
            kat = r.get("kategori", "").strip().lower()

            freq_count = 1
            if qr and qr in qr_counter:
                freq_count = max(freq_count, qr_counter[qr])
            if lok and lok in location_counter:
                freq_count = max(freq_count, location_counter[lok])
            if kat and kat in kategori_counter:
                # Ambil proporsi kategori jika ada konsentrasi kerusakan
                freq_count = max(freq_count, min(5, kategori_counter[kat]))

            frekuensi_nilai = min(100.0, float(freq_count * 20))
            frekuensi_subskor = round(frekuensi_nilai * 0.30, 2)

            # 3. Dampak Fasilitas terhadap Kegiatan Kampus (Weight 30%)
            kat_nama = r.get("kategori", "").lower()
            lok_nama = r.get("lokasi", "").lower()

            if any(k in kat_nama for k in ["ac", "listrik", "proyektor", "plafon", "laboratorium", "server", "pipa", "atap"]):
                dampak_nilai = 95.0
                dampak_keterangan = "Fasilitas vital penunjang langsung kelancaran perkuliahan dan laboratorium."
            elif any(k in kat_nama for k in ["toilet", "pintu", "jendela", "lampu", "kran", "wastafel", "air"]):
                dampak_nilai = 75.0
                dampak_keterangan = "Fasilitas umum penunjang sanitasi, keamanan, dan sirkulasi ruangan."
            else:
                dampak_nilai = 50.0
                dampak_keterangan = "Fasilitas perabot individual/furnitur pendukung kenyamanan ruangan."

            # Bonus dampak jika berada di Lab, Ruang Ujian, atau Ruang Kelas Utama
            if any(area in lok_nama for area in ["lab", "ujian", "auditorium", "ruang kuliah", "server"]):
                dampak_nilai = min(100.0, dampak_nilai + 10.0)

            dampak_subskor = round(dampak_nilai * 0.30, 2)

            # Skor Urgensi Komposit (0 - 100)
            skor_urgensi = int(round(keparahan_subskor + frekuensi_subskor + dampak_subskor))
            skor_urgensi = max(0, min(100, skor_urgensi))

            # Klasifikasi Kategori Prioritas
            if skor_urgensi > 80:
                kategori_prioritas = "Tinggi"
                rekomendasi_tindakan = "Prioritas Utama: Segera lakukan perbaikan darurat oleh tim teknisi dalam waktu 1x24 jam."
            elif skor_urgensi >= 50:
                kategori_prioritas = "Sedang"
                rekomendasi_tindakan = "Prioritas Standar: Jadwalkan perbaikan reguler dan siapkan suku cadang dalam 2-3 hari kerja."
            else:
                kategori_prioritas = "Rendah"
                rekomendasi_tindakan = "Prioritas Rendah: Masukkan ke jadwal pemeliharaan berkala fasilitas mingguan."

            prioritized.append({
                "id_laporan": r.get("id_laporan"),
                "nomor_tiket": r.get("nomor_tiket"),
                "id_user": r.get("id_user"),
                "nama_pelapor": r.get("nama_pelapor", "Pelapor"),
                "nomor_induk_pelapor": r.get("nomor_induk_pelapor") or r.get("nomor_induk") or "12345678",
                "kategori": r.get("kategori", "Umum"),
                "lokasi": r.get("lokasi", "Kampus"),
                "tingkat_keparahan": r.get("tingkat_keparahan", "Sedang"),
                "status": r.get("status", "Diajukan"),
                "foto_url": r.get("foto_url", ""),
                "kode_qr": r.get("kode_qr"),
                "skor_urgensi": skor_urgensi,
                "kategori_prioritas": kategori_prioritas,
                "rekomendasi_tindakan": rekomendasi_tindakan,
                "breakdown": {
                    "keparahan_nilai": keparahan_nilai,
                    "keparahan_bobot": 0.40,
                    "keparahan_subskor": keparahan_subskor,
                    "frekuensi_nilai": frekuensi_nilai,
                    "frekuensi_bobot": 0.30,
                    "frekuensi_subskor": frekuensi_subskor,
                    "frekuensi_count": freq_count,
                    "dampak_nilai": dampak_nilai,
                    "dampak_bobot": 0.30,
                    "dampak_subskor": dampak_subskor,
                    "dampak_keterangan": dampak_keterangan
                },
                "created_at": r.get("created_at", "")
            })

        # Urutkan berdasarkan skor urgensi tertinggi, lalu created_at terbaru
        prioritized.sort(key=lambda x: (x["skor_urgensi"], x["created_at"]), reverse=True)

        # Sematkan Rank #1, #2, dst.
        for idx, item in enumerate(prioritized):
            item["rank"] = idx + 1

        return prioritized

gemini_analytics = GeminiAnalyticsService()
