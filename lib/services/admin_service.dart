import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/admin_model.dart';
import '../models/report_model.dart';
import 'api_service.dart';

class AdminService {
  final http.Client _client = http.Client();

  Future<AdminDashboardSummaryModel> getDashboardSummary() async {
    final url = Uri.parse('${ApiService.baseUrl}/api/v1/admin/dashboard/summary');
    final response = await _client.get(url);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return AdminDashboardSummaryModel.fromJson(data);
    } else {
      throw Exception('Gagal memuat ringkasan dashboard admin.');
    }
  }

  Future<Map<String, dynamic>> getAdminReports({String? statusFilter}) async {
    String query = '';
    if (statusFilter != null && statusFilter.isNotEmpty && statusFilter != 'Semua') {
      query = '?status_filter=$statusFilter';
    }
    final url = Uri.parse('${ApiService.baseUrl}/api/v1/admin/laporan$query');
    final response = await _client.get(url);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final rawList = data['laporan'] as List? ?? [];
      final reports = rawList.map((e) => ReportModel.fromJson(e)).toList();
      return {
        'total_laporan': data['total_laporan'] ?? reports.length,
        'menunggu_peninjauan': data['menunggu_peninjauan'] ?? 0,
        'laporan': reports,
      };
    } else {
      throw Exception('Gagal memuat daftar laporan admin.');
    }
  }

  Future<AdminUpdateStatusResult> updateReportStatus({
    required String idLaporan,
    required String status,
    String? aksiTeknis,
    String? catatan,
    String? alasanPenolakan,
    String adminId = 'USR-002',
    String adminName = 'Administrator Fasilitas',
  }) async {
    final cleanId = idLaporan.trim().replaceAll('#', '');
    final url = Uri.parse('${ApiService.baseUrl}/api/v1/admin/laporan/$cleanId/status');

    final payload = {
      'status': status,
      'aksi_teknis': aksiTeknis,
      'catatan': catatan,
      'alasan_penolakan': alasanPenolakan,
      'admin_id': adminId,
      'admin_name': adminName,
    };

    final response = await _client.put(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(payload),
    );

    final data = jsonDecode(response.body);
    if (response.statusCode == 200) {
      return AdminUpdateStatusResult.fromJson(data);
    } else {
      final err = data['detail'] ?? data['message'] ?? 'Gagal memperbarui status laporan.';
      throw Exception(err);
    }
  }
}
