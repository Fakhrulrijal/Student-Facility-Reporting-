import 'dart:io' show Platform;
import 'package:flutter/foundation.dart';

class ApiService {
  // Secara otomatis memilih host yang tepat sesuai platform eksekusi
  static String get baseUrl {
    if (kIsWeb) {
      return 'http://127.0.0.1:8000';
    }
    try {
      if (Platform.isAndroid) {
        return 'http://10.0.2.2:8000'; // Default Android Emulator
      }
    } catch (_) {}
    return 'http://127.0.0.1:8000';
  }
}
