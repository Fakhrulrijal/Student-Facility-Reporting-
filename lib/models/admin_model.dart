class AdminDashboardSummaryModel {
  final int totalLaporan;
  final int menungguPeninjauan;
  final int diproses;
  final int selesai;
  final int ditolak;
  final Map<String, int> breakdownKategori;

  AdminDashboardSummaryModel({
    required this.totalLaporan,
    required this.menungguPeninjauan,
    required this.diproses,
    required this.selesai,
    required this.ditolak,
    required this.breakdownKategori,
  });

  factory AdminDashboardSummaryModel.fromJson(Map<String, dynamic> json) {
    Map<String, int> breakdown = {};
    if (json['breakdown_kategori'] != null) {
      json['breakdown_kategori'].forEach((k, v) {
        breakdown[k] = (v as num).toInt();
      });
    }

    return AdminDashboardSummaryModel(
      totalLaporan: json['total_laporan'] ?? 0,
      menungguPeninjauan: json['menunggu_peninjauan'] ?? 0,
      diproses: json['diproses'] ?? 0,
      selesai: json['selesai'] ?? 0,
      ditolak: json['ditolak'] ?? 0,
      breakdownKategori: breakdown,
    );
  }
}

class AdminUpdateStatusResult {
  final String idLaporan;
  final String nomorTiket;
  final String statusBaru;
  final String? aksiTeknis;
  final String? catatan;
  final String? alasanPenolakan;
  final String notificationTitle;
  final String notificationBody;
  final String message;

  AdminUpdateStatusResult({
    required this.idLaporan,
    required this.nomorTiket,
    required this.statusBaru,
    this.aksiTeknis,
    this.catatan,
    this.alasanPenolakan,
    required this.notificationTitle,
    required this.notificationBody,
    required this.message,
  });

  factory AdminUpdateStatusResult.fromJson(Map<String, dynamic> json) {
    final notif = json['notification'] ?? {};
    return AdminUpdateStatusResult(
      idLaporan: json['id_laporan'] ?? '',
      nomorTiket: json['nomor_tiket'] ?? '',
      statusBaru: json['status_baru'] ?? '',
      aksiTeknis: json['aksi_teknis'],
      catatan: json['catatan'],
      alasanPenolakan: json['alasan_penolakan'],
      notificationTitle: notif['title'] ?? 'Update Tiket',
      notificationBody: notif['body'] ?? 'Status laporan telah diperbarui.',
      message: json['message'] ?? 'Perubahan tersimpan di database.',
    );
  }
}
