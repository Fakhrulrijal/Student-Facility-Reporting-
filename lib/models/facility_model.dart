class FacilityModel {
  final String idFasilitas;
  final String kodeQr;
  final String namaFasilitas;
  final String lokasiGedung;
  final String kategori;
  final String? kondisiTerakhir;

  FacilityModel({
    required this.idFasilitas,
    required this.kodeQr,
    required this.namaFasilitas,
    required this.lokasiGedung,
    required this.kategori,
    this.kondisiTerakhir = 'Normal',
  });

  factory FacilityModel.fromJson(Map<String, dynamic> json) {
    return FacilityModel(
      idFasilitas: json['id_fasilitas'] ?? '',
      kodeQr: json['kode_qr'] ?? '',
      namaFasilitas: json['nama_fasilitas'] ?? '',
      lokasiGedung: json['lokasi_gedung'] ?? '',
      kategori: json['kategori'] ?? '',
      kondisiTerakhir: json['kondisi_terakhir'] ?? 'Normal',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id_fasilitas': idFasilitas,
      'kode_qr': kodeQr,
      'nama_fasilitas': namaFasilitas,
      'lokasi_gedung': lokasiGedung,
      'kategori': kategori,
      'kondisi_terakhir': kondisiTerakhir,
    };
  }
}
