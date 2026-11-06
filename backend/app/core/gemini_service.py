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

gemini_analytics = GeminiAnalyticsService()
