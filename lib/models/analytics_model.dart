class ExecutiveSummaryModel {
  final bool found;
  final String? idAnalisis;
  final String filterLabel;
  final int totalLaporan;
  final List<String> bullets;
  final String rekomendasi;
  final Map<String, dynamic> statistik;
  final String createdAt;

  ExecutiveSummaryModel({
    required this.found,
    this.idAnalisis,
    required this.filterLabel,
    required this.totalLaporan,
    required this.bullets,
    required this.rekomendasi,
    required this.statistik,
    required this.createdAt,
  });

  factory ExecutiveSummaryModel.fromJson(Map<String, dynamic> json) {
    var rawBullets = json['bullets'] as List? ?? [];
    List<String> bulletList = rawBullets.map((e) => e.toString()).toList();

    return ExecutiveSummaryModel(
      found: json['found'] ?? true,
      idAnalisis: json['id_analisis'],
      filterLabel: json['filter_label'] ?? 'Semua Laporan',
      totalLaporan: json['total_laporan'] ?? 0,
      bullets: bulletList,
      rekomendasi: json['rekomendasi'] ?? '',
      statistik: json['statistik'] as Map<String, dynamic>? ?? {},
      createdAt: json['created_at'] ?? '',
    );
  }
}
