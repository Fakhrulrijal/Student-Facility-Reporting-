import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/analytics_model.dart';
import 'api_service.dart';

class AnalyticsService {
  final http.Client _client = http.Client();

  Future<ExecutiveSummaryModel> generateSummary({
    required String periode,
    required String gedung,
    required String kategori,
  }) async {
    final url = Uri.parse('${ApiService.baseUrl}/api/v1/analytics/summary');
    final response = await _client.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'periode': periode,
        'gedung': gedung,
        'kategori': kategori,
      }),
    );

    final data = jsonDecode(response.body);
    if (response.statusCode == 200) {
      return ExecutiveSummaryModel.fromJson(data);
    } else {
      final msg = data['detail'] ?? data['message'] ?? 'Gagal membuat rangkuman AI.';
      throw Exception(msg);
    }
  }
}
