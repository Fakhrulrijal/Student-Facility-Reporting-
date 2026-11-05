import 'package:flutter/foundation.dart';
import '../models/facility_model.dart';
import '../models/report_model.dart';
import '../models/timeline_model.dart';
import '../services/report_service.dart';

class ReportProvider with ChangeNotifier {
  final ReportService _reportService = ReportService();

  // Form State
  String? _photoPath;
  Uint8List? _photoBytes;
  String? _photoName;

  FacilityModel? _scannedFacility;
  String _lokasi = '';
  String _kategori = 'Kursi';
  String _tingkatKeparahan = 'Sedang';
  String _deskripsi = '';
  String? _kodeQr;

  bool _isScanning = false;
  bool _isSubmitting = false;
  String? _scanError;
  String? _submitError;

  ReportModel? _lastSubmittedReport;
  List<ReportModel> _reports = [];

  // MOD-03 State
  List<ReportModel> _userReports = [];
  bool _isLoadingUserReports = false;
  String? _userReportsError;
  String _selectedTab = 'Semua'; // 'Semua', 'Diproses', 'Selesai'

  ReportHistoryModel? _currentReportHistory;
  bool _isLoadingHistory = false;
  String? _historyError;

  // Getters
  String? get photoPath => _photoPath;
  Uint8List? get photoBytes => _photoBytes;
  String? get photoName => _photoName;
  FacilityModel? get scannedFacility => _scannedFacility;
  String get lokasi => _lokasi;
  String get kategori => _kategori;
  String get tingkatKeparahan => _tingkatKeparahan;
  String get deskripsi => _deskripsi;
  String? get kodeQr => _kodeQr;
  bool get isScanning => _isScanning;
  bool get isSubmitting => _isSubmitting;
  String? get scanError => _scanError;
  String? get submitError => _submitError;
  ReportModel? get lastSubmittedReport => _lastSubmittedReport;
  List<ReportModel> get reports => _reports;

  // MOD-03 Getters
  List<ReportModel> get userReports => _userReports;
  bool get isLoadingUserReports => _isLoadingUserReports;
  String? get userReportsError => _userReportsError;
  String get selectedTab => _selectedTab;
  ReportHistoryModel? get currentReportHistory => _currentReportHistory;
  bool get isLoadingHistory => _isLoadingHistory;
  String? get historyError => _historyError;

  // Filtered reports for current tab
  List<ReportModel> get filteredUserReports {
    if (_selectedTab == 'Semua') return _userReports;
    return _userReports.where((r) => r.status.toLowerCase() == _selectedTab.toLowerCase()).toList();
  }

  void setSelectedTab(String tab) {
    _selectedTab = tab;
    notifyListeners();
  }

  Future<void> fetchUserReports(String userId) async {
    _isLoadingUserReports = true;
    _userReportsError = null;
    notifyListeners();

    try {
      final list = await _reportService.getUserReports(userId);
      _userReports = list;
      _isLoadingUserReports = false;
      notifyListeners();
    } catch (e) {
      _isLoadingUserReports = false;
      _userReportsError = e.toString().replaceAll('Exception: ', '');
      notifyListeners();
    }
  }

  Future<void> fetchReportHistory(String idLaporan) async {
    _isLoadingHistory = true;
    _historyError = null;
    notifyListeners();

    try {
      final hist = await _reportService.getReportHistory(idLaporan);
      _currentReportHistory = hist;
      _isLoadingHistory = false;
      notifyListeners();
    } catch (e) {
      _isLoadingHistory = false;
      _historyError = e.toString().replaceAll('Exception: ', '');
      notifyListeners();
    }
  }

  void setPhoto(String path, {Uint8List? bytes, String? name}) {
    _photoPath = path;
    _photoBytes = bytes;
    _photoName = name ?? 'kerusakan_${DateTime.now().millisecondsSinceEpoch}.jpg';
    notifyListeners();
  }

  void setFormFields({
    String? lokasi,
    String? kategori,
    String? tingkatKeparahan,
    String? deskripsi,
    String? kodeQr,
  }) {
    if (lokasi != null) _lokasi = lokasi;
    if (kategori != null) _kategori = kategori;
    if (tingkatKeparahan != null) _tingkatKeparahan = tingkatKeparahan;
    if (deskripsi != null) _deskripsi = deskripsi;
    if (kodeQr != null) _kodeQr = kodeQr;
    notifyListeners();
  }

  Future<bool> checkQrCode(String qrCode) async {
    _isScanning = true;
    _scanError = null;
    notifyListeners();

    try {
      final facility = await _reportService.checkQrCode(qrCode);
      _scannedFacility = facility;
      _kodeQr = facility.kodeQr;
      _lokasi = facility.lokasiGedung;
      _kategori = facility.kategori;
      _isScanning = false;
      notifyListeners();
      return true;
    } catch (e) {
      _isScanning = false;
      _scannedFacility = null;
      _scanError = e.toString().replaceAll('Exception: ', '');
      notifyListeners();
      return false;
    }
  }

  void applyScannedData() {
    if (_scannedFacility != null) {
      _lokasi = _scannedFacility!.lokasiGedung;
      _kategori = _scannedFacility!.kategori;
      _kodeQr = _scannedFacility!.kodeQr;
      notifyListeners();
    }
  }

  void clearQrError() {
    _scanError = null;
    notifyListeners();
  }

  Future<bool> submitReport({String? token}) async {
    _isSubmitting = true;
    _submitError = null;
    notifyListeners();

    try {
      final report = await _reportService.submitReport(
        filePath: _photoPath ?? '',
        fileBytes: _photoBytes,
        fileName: _photoName,
        lokasi: _lokasi,
        kategori: _kategori,
        tingkatKeparahan: _tingkatKeparahan,
        deskripsi: _deskripsi,
        kodeQr: _kodeQr,
        token: token,
      );
      _lastSubmittedReport = report;
      _reports.insert(0, report);
      _isSubmitting = false;
      notifyListeners();
      return true;
    } catch (e) {
      _isSubmitting = false;
      _submitError = e.toString().replaceAll('Exception: ', '');
      notifyListeners();
      return false;
    }
  }

  void resetForm() {
    _photoPath = null;
    _photoBytes = null;
    _photoName = null;
    _scannedFacility = null;
    _lokasi = '';
    _kategori = 'Kursi';
    _tingkatKeparahan = 'Sedang';
    _deskripsi = '';
    _kodeQr = null;
    _scanError = null;
    _submitError = null;
    notifyListeners();
  }
}
