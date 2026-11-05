import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/user_model.dart';
import 'api_service.dart';

class AuthService {
  final http.Client _client = http.Client();

  Future<Map<String, dynamic>> login(String identifier, String password) async {
    final url = Uri.parse('${ApiService.baseUrl}/api/v1/auth/login');
    final response = await _client.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'nomor_induk_atau_email': identifier,
        'password': password,
      }),
    );

    final data = jsonDecode(response.body);
    if (response.statusCode == 200) {
      return {
        'token': data['access_token'],
        'user': UserModel.fromJson(data['user']),
      };
    } else {
      final errorMsg = data['detail'] ?? data['message'] ?? 'Login gagal. Periksa kredensial Anda.';
      throw Exception(errorMsg);
    }
  }

  Future<Map<String, dynamic>> register({
    required String nama,
    required String nomorInduk,
    required String email,
    required String password,
    required String role,
  }) async {
    final url = Uri.parse('${ApiService.baseUrl}/api/v1/auth/register');
    final response = await _client.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'nama': nama,
        'nomor_induk': nomorInduk,
        'email': email,
        'password': password,
        'role': role,
      }),
    );

    final data = jsonDecode(response.body);
    if (response.statusCode == 201) {
      return {
        'token': data['access_token'],
        'user': UserModel.fromJson(data['user']),
      };
    } else {
      String errorMsg = 'Registrasi gagal.';
      if (data['errors'] != null && data['errors'] is List) {
        errorMsg = (data['errors'] as List).join('\n');
      } else if (data['detail'] != null) {
        errorMsg = data['detail'].toString();
      }
      throw Exception(errorMsg);
    }
  }
}
