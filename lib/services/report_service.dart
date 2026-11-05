import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/facility_model.dart';
import '../models/report_model.dart';
import 'api_service.dart';

class ReportService {
  final http.Client _client = http.Client();

  // Scan QR Code Fasilitas
  Future<FacilityModel> checkQrCode(String kodeQr) async {
    final cleanCode = kodeQr.trim();
    final url = Uri.parse('${ApiService.baseUrl}/api/v1/fasilitas/qr/$cleanCode');
    final response = await _client.get(url);

    final data = jsonDecode(response.body);
    if (response.statusCode == 200) {
      return FacilityModel.fromJson(data);
    } else {
      final msg = data['detail'] ?? 'Kode bukan milik fasilitas kampus atau rusak.';
      throw Exception(msg);
    }
  }

  // Kirim Formulir Laporan (Multipart Form-Data)
  Future<ReportModel> submitReport({
    required String filePath,
    List<int>? fileBytes,
    String? fileName,
    required String lokasi,
    required String kategori,
    required String tingkatKeparahan,
    required String deskripsi,
    String? kodeQr,
    String? token,
  }) async {
    final url = Uri.parse('${ApiService.baseUrl}/api/v1/laporan');
    final request = http.MultipartRequest('POST', url);

    if (token != null && token.isNotEmpty) {
      request.headers['Authorization'] = 'Bearer $token';
    }

    request.fields['lokasi'] = lokasi;
    request.fields['kategori'] = kategori;
    request.fields['tingkat_keparahan'] = tingkatKeparahan;
    request.fields['deskripsi'] = deskripsi;
    if (kodeQr != null && kodeQr.isNotEmpty) {
      request.fields['kode_qr'] = kodeQr;
    }

    if (fileBytes != null && fileName != null) {
      request.files.add(http.MultipartFile.fromBytes('foto', fileBytes, filename: fileName));
    } else if (filePath.isNotEmpty) {
      request.files.add(await http.MultipartFile.fromPath('foto', filePath));
    }

    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);
    final data = jsonDecode(response.body);

    if (response.statusCode == 201) {
      return ReportModel(
        idLaporan: data['id_laporan'] ?? '',
        nomorTiket: data['nomor_tiket'] ?? '#TK-0012',
        lokasi: data['lokasi'] ?? lokasi,
        kategori: data['kategori'] ?? kategori,
        tingkatKeparahan: data['tingkat_keparahan'] ?? tingkatKeparahan,
        deskripsi: data['deskripsi'] ?? deskripsi,
        fotoUrl: data['foto_url'] ?? '',
        status: data['status'] ?? 'Diajukan',
        kodeQr: data['kode_qr'],
        createdAt: data['created_at'] ?? '',
      );
    } else {
      final msg = data['detail'] ?? data['message'] ?? 'Gagal mengirimkan laporan.';
      throw Exception(msg);
    }
  }

  // Ambil Riwayat Laporan
  Future<List<ReportModel>> getReports() async {
    final url = Uri.parse('${ApiService.baseUrl}/api/v1/laporan');
    final response = await _client.get(url);
    if (response.statusCode == 200) {
      final List<dynamic> list = jsonDecode(response.body);
      return list.map((e) => ReportModel.fromJson(e)).toList();
    } else {
      throw Exception('Gagal memuat histori laporan.');
    }
  }
}
