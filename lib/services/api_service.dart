import 'dart:io' show Platform;
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  // IP Laptop server di jaringan Wi-Fi lokal saat ini
  static String customHost = '192.168.1.8';

  // Inisialisasi membaca IP yang tersimpan dari memori HP
  static Future<void> init() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final savedHost = prefs.getString('server_host');
      if (savedHost != null && savedHost.trim().isNotEmpty) {
        customHost = savedHost.trim();
      }
    } catch (_) {}
  }

  // Mengubah IP Server secara dinamis dari aplikasi
  static Future<void> setHost(String newHost) async {
    customHost = newHost.trim();
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('server_host', customHost);
    } catch (_) {}
  }

  // Secara otomatis memilih host yang tepat sesuai platform eksekusi
  static String get baseUrl {
    if (kIsWeb) {
      final host = Uri.base.host.isNotEmpty ? Uri.base.host : '127.0.0.1';
      return 'http://$host:8000';
    }
    try {
      if (Platform.isAndroid) {
        // Untuk perangkat fisik Android di jaringan Wi-Fi yang sama
        return 'http://$customHost:8000';
      }
    } catch (_) {}
    return 'http://127.0.0.1:8000';
  }
}
