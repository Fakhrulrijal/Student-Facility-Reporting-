import 'package:flutter/foundation.dart';
import '../models/analytics_model.dart';
import '../services/analytics_service.dart';

class AnalyticsProvider with ChangeNotifier {
  final AnalyticsService _analyticsService = AnalyticsService();

  String _selectedPeriode = 'Oktober 2026';
  String _selectedGedung = 'Semua Gedung';
  String _selectedKategori = 'Semua Kategori';

  ExecutiveSummaryModel? _summaryResult;
  bool _isGenerating = false;
  String? _error;
  bool _hasGenerated = false;

  // Getters
  String get selectedPeriode => _selectedPeriode;
  String get selectedGedung => _selectedGedung;
  String get selectedKategori => _selectedKategori;
  ExecutiveSummaryModel? get summaryResult => _summaryResult;
  bool get isGenerating => _isGenerating;
  String? get error => _error;
  bool get hasGenerated => _hasGenerated;

  void setPeriode(String val) {
    _selectedPeriode = val;
    notifyListeners();
  }

  void setGedung(String val) {
    _selectedGedung = val;
    notifyListeners();
  }

  void setKategori(String val) {
    _selectedKategori = val;
    notifyListeners();
  }

  void resetFilter() {
    _hasGenerated = false;
    _summaryResult = null;
    _error = null;
    notifyListeners();
  }

  Future<void> generateSummary() async {
    _isGenerating = true;
    _error = null;
    notifyListeners();

    try {
      final res = await _analyticsService.generateSummary(
        periode: _selectedPeriode,
        gedung: _selectedGedung,
        kategori: _selectedKategori,
      );
      _summaryResult = res;
      _hasGenerated = true;
      _isGenerating = false;
      notifyListeners();
    } catch (e) {
      _isGenerating = false;
      _error = e.toString().replaceAll('Exception: ', '');
      notifyListeners();
    }
  }

  void simulateDataNotFound() {
    _isGenerating = false;
    _summaryResult = ExecutiveSummaryModel(
      found: false,
      filterLabel: 'Januari 2020 · Gedung Antariksa · Helikopter',
      totalLaporan: 0,
      bullets: [],
      rekomendasi: 'Tidak ada laporan yang sesuai dengan filter yang dipilih.',
      statistik: {},
      createdAt: DateTime.now().toIso8601String(),
    );
    _hasGenerated = true;
    notifyListeners();
  }
}
