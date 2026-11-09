import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/priority_model.dart';
import 'api_service.dart';

class PriorityService {
  final http.Client _client = http.Client();

  // Mengambil daftar tiket yang telah diperingkatkan (GET)
  Future<Map<String, dynamic>> fetchPrioritizedTickets({
    String status = 'Semua',
    String prioritas = 'Semua',
    String gedung = 'Semua Gedung',
  }) async {
    final uri = Uri.parse('${ApiService.baseUrl}/api/v1/ai/prioritized-tickets').replace(
      queryParameters: {
        'status_filter': status,
        'kategori_prioritas': prioritas,
        'gedung': gedung,
      },
    );

    final response = await _client.get(
      uri,
      headers: {'Accept': 'application/json'},
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final summary = PrioritySummaryModel.fromJson(data['summary'] ?? {});
      final List<dynamic> listJson = data['tickets'] ?? [];
      final tickets = listJson.map((t) => PrioritizedTicketModel.fromJson(t)).toList();

      return {
        'summary': summary,
        'tickets': tickets,
        'timestamp': data['timestamp'] ?? '',
      };
    } else {
      throw Exception('Gagal memuat daftar prioritas tiket (Status: ${response.statusCode})');
    }
  }

  // Memicu kalkulasi ulang skor prioritas (POST)
  Future<Map<String, dynamic>> recalculatePriorities({
    String status = 'Semua',
    String prioritas = 'Semua',
    String gedung = 'Semua Gedung',
  }) async {
    final url = Uri.parse('${ApiService.baseUrl}/api/v1/ai/prioritize-tickets');

    final response = await _client.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'status_filter': status,
        'kategori_prioritas': prioritas,
        'gedung': gedung,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final summary = PrioritySummaryModel.fromJson(data['summary'] ?? {});
      final List<dynamic> listJson = data['tickets'] ?? [];
      final tickets = listJson.map((t) => PrioritizedTicketModel.fromJson(t)).toList();

      return {
        'summary': summary,
        'tickets': tickets,
        'timestamp': data['timestamp'] ?? '',
      };
    } else {
      throw Exception('Gagal mengkalkulasi ulang prioritas AI.');
    }
  }

  // Mengambil rincian breakdown kalkulasi untuk satu tiket
  Future<PrioritizedTicketModel> getTicketPriorityDetail(String idLaporan) async {
    final cleanId = idLaporan.replaceAll('#', '');
    final url = Uri.parse('${ApiService.baseUrl}/api/v1/ai/prioritize-ticket/$cleanId');

    final response = await _client.get(
      url,
      headers: {'Accept': 'application/json'},
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return PrioritizedTicketModel.fromJson(data);
    } else {
      throw Exception('Gagal mengambil detail skor prioritas tiket.');
    }
  }
}
