class TimelineStageModel {
  final String stageKey;
  final String stageName;
  final bool isCompleted;
  final bool isCurrent;
  final String? timestamp;
  final String? catatan;
  final String? petugas;

  TimelineStageModel({
    required this.stageKey,
    required this.stageName,
    required this.isCompleted,
    required this.isCurrent,
    this.timestamp,
    this.catatan,
    this.petugas,
  });

  factory TimelineStageModel.fromJson(Map<String, dynamic> json) {
    return TimelineStageModel(
      stageKey: json['stage_key'] ?? '',
      stageName: json['stage_name'] ?? '',
      isCompleted: json['is_completed'] ?? false,
      isCurrent: json['is_current'] ?? false,
      timestamp: json['timestamp'],
      catatan: json['catatan'],
      petugas: json['petugas'],
    );
  }
}

class ReportHistoryModel {
  final String idLaporan;
  final String nomorTiket;
  final String statusSaatIni;
  final List<TimelineStageModel> timeline;

  ReportHistoryModel({
    required this.idLaporan,
    required this.nomorTiket,
    required this.statusSaatIni,
    required this.timeline,
  });

  factory ReportHistoryModel.fromJson(Map<String, dynamic> json) {
    var rawList = json['timeline'] as List? ?? [];
    List<TimelineStageModel> stages = rawList.map((e) => TimelineStageModel.fromJson(e)).toList();

    return ReportHistoryModel(
      idLaporan: json['id_laporan'] ?? '',
      nomorTiket: json['nomor_tiket'] ?? '',
      statusSaatIni: json['status_saat_ini'] ?? 'Diajukan',
      timeline: stages,
    );
  }
}
