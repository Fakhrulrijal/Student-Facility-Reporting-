class ScoreBreakdown {
  final double keparahanNilai;
  final double keparahanBobot;
  final double keparahanSubskor;
  final double frekuensiNilai;
  final double frekuensiBobot;
  final double frekuensiSubskor;
  final int frekuensiCount;
  final double dampakNilai;
  final double dampakBobot;
  final double dampakSubskor;
  final String dampakKeterangan;

  ScoreBreakdown({
    required this.keparahanNilai,
    required this.keparahanBobot,
    required this.keparahanSubskor,
    required this.frekuensiNilai,
    required this.frekuensiBobot,
    required this.frekuensiSubskor,
    required this.frekuensiCount,
    required this.dampakNilai,
    required this.dampakBobot,
    required this.dampakSubskor,
    required this.dampakKeterangan,
  });

  factory ScoreBreakdown.fromJson(Map<String, dynamic> json) {
    return ScoreBreakdown(
      keparahanNilai: (json['keparahan_nilai'] as num?)?.toDouble() ?? 0.0,
      keparahanBobot: (json['keparahan_bobot'] as num?)?.toDouble() ?? 0.40,
      keparahanSubskor: (json['keparahan_subskor'] as num?)?.toDouble() ?? 0.0,
      frekuensiNilai: (json['frekuensi_nilai'] as num?)?.toDouble() ?? 0.0,
      frekuensiBobot: (json['frekuensi_bobot'] as num?)?.toDouble() ?? 0.30,
      frekuensiSubskor: (json['frekuensi_subskor'] as num?)?.toDouble() ?? 0.0,
      frekuensiCount: (json['frekuensi_count'] as num?)?.toInt() ?? 1,
      dampakNilai: (json['dampak_nilai'] as num?)?.toDouble() ?? 0.0,
      dampakBobot: (json['dampak_bobot'] as num?)?.toDouble() ?? 0.30,
      dampakSubskor: (json['dampak_subskor'] as num?)?.toDouble() ?? 0.0,
      dampakKeterangan: json['dampak_keterangan'] ?? '',
    );
  }
}

class PrioritizedTicketModel {
  final int rank;
  final String idLaporan;
  final String nomorTiket;
  final String? idUser;
  final String? namaPelapor;
  final String? nomorIndukPelapor;
  final String kategori;
  final String lokasi;
  final String tingkatKeparahan;
  final String status;
  final String fotoUrl;
  final String? kodeQr;
  final int skorUrgensi;
  final String kategoriPrioritas; // Tinggi, Sedang, Rendah
  final String rekomendasiTindakan;
  final ScoreBreakdown breakdown;
  final String createdAt;

  PrioritizedTicketModel({
    required this.rank,
    required this.idLaporan,
    required this.nomorTiket,
    this.idUser,
    this.namaPelapor,
    this.nomorIndukPelapor,
    required this.kategori,
    required this.lokasi,
    required this.tingkatKeparahan,
    required this.status,
    required this.fotoUrl,
    this.kodeQr,
    required this.skorUrgensi,
    required this.kategoriPrioritas,
    required this.rekomendasiTindakan,
    required this.breakdown,
    required this.createdAt,
  });

  factory PrioritizedTicketModel.fromJson(Map<String, dynamic> json) {
    return PrioritizedTicketModel(
      rank: (json['rank'] as num?)?.toInt() ?? 1,
      idLaporan: json['id_laporan'] ?? '',
      nomorTiket: json['nomor_tiket'] ?? '',
      idUser: json['id_user'],
      namaPelapor: json['nama_pelapor'],
      nomorIndukPelapor: json['nomor_induk_pelapor'],
      kategori: json['kategori'] ?? 'Umum',
      lokasi: json['lokasi'] ?? '',
      tingkatKeparahan: json['tingkat_keparahan'] ?? 'Sedang',
      status: json['status'] ?? 'Diajukan',
      fotoUrl: json['foto_url'] ?? '',
      kodeQr: json['kode_qr'],
      skorUrgensi: (json['skor_urgensi'] as num?)?.toInt() ?? 50,
      kategoriPrioritas: json['kategori_prioritas'] ?? 'Sedang',
      rekomendasiTindakan: json['rekomendasi_tindakan'] ?? '',
      breakdown: ScoreBreakdown.fromJson(json['breakdown'] ?? {}),
      createdAt: json['created_at'] ?? '',
    );
  }
}

class PrioritySummaryModel {
  final int totalEvaluated;
  final int totalTinggi;
  final int totalSedang;
  final int totalRendah;
  final double averageScore;

  PrioritySummaryModel({
    required this.totalEvaluated,
    required this.totalTinggi,
    required this.totalSedang,
    required this.totalRendah,
    required this.averageScore,
  });

  factory PrioritySummaryModel.fromJson(Map<String, dynamic> json) {
    return PrioritySummaryModel(
      totalEvaluated: (json['total_evaluated'] as num?)?.toInt() ?? 0,
      totalTinggi: (json['total_tinggi'] as num?)?.toInt() ?? 0,
      totalSedang: (json['total_sedang'] as num?)?.toInt() ?? 0,
      totalRendah: (json['total_rendah'] as num?)?.toInt() ?? 0,
      averageScore: (json['average_score'] as num?)?.toDouble() ?? 0.0,
    );
  }
}
