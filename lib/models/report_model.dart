class ReportModel {
  final String idLaporan;
  final String nomorTiket;
  final String? idUser;
  final String? namaPelapor;
  final String? nomorIndukPelapor;
  final String? idFasilitas;
  final String? kodeQr;
  final String lokasi;
  final String kategori;
  final String tingkatKeparahan;
  final String deskripsi;
  final String fotoUrl;
  final String status;
  final String createdAt;

  ReportModel({
    required this.idLaporan,
    required this.nomorTiket,
    this.idUser,
    this.namaPelapor,
    this.nomorIndukPelapor,
    this.idFasilitas,
    this.kodeQr,
    required this.lokasi,
    required this.kategori,
    required this.tingkatKeparahan,
    required this.deskripsi,
    required this.fotoUrl,
    required this.status,
    required this.createdAt,
  });

  factory ReportModel.fromJson(Map<String, dynamic> json) {
    return ReportModel(
      idLaporan: json['id_laporan'] ?? '',
      nomorTiket: json['nomor_tiket'] ?? '',
      idUser: json['id_user'],
      namaPelapor: json['nama_pelapor'],
      nomorIndukPelapor: json['nomor_induk_pelapor'] ?? json['nomor_induk'],
      idFasilitas: json['id_fasilitas'],
      kodeQr: json['kode_qr'],
      lokasi: json['lokasi'] ?? '',
      kategori: json['kategori'] ?? '',
      tingkatKeparahan: json['tingkat_keparahan'] ?? 'Sedang',
      deskripsi: json['deskripsi'] ?? '',
      fotoUrl: json['foto_url'] ?? '',
      status: json['status'] ?? 'Diajukan',
      createdAt: json['created_at'] ?? '',
    );
  }
}
