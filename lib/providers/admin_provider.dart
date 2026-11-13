import 'package:flutter/foundation.dart';
import '../models/admin_model.dart';
import '../models/report_model.dart';
import '../services/admin_service.dart';

class AdminProvider with ChangeNotifier {
  final AdminService _adminService = AdminService();

  AdminDashboardSummaryModel? _summary;
  List<ReportModel> _adminReports = [];
  int _totalLaporan = 0;
  int _menungguPeninjauan = 0;
  String _selectedTab = 'Semua';
  String _selectedCategory = 'Semua';

  bool _isLoading = false;
  bool _isUpdating = false;
  String? _error;

  ReportModel? _selectedReportForAction;
  AdminUpdateStatusResult? _lastUpdatedResult;

  // Getters
  AdminDashboardSummaryModel? get summary => _summary;
  List<ReportModel> get adminReports => _adminReports;
  int get totalLaporan => _totalLaporan;
  int get menungguPeninjauan => _menungguPeninjauan;
  String get selectedTab => _selectedTab;
  String get selectedCategory => _selectedCategory;
  bool get isLoading => _isLoading;
  bool get isUpdating => _isUpdating;
  String? get error => _error;
  ReportModel? get selectedReportForAction => _selectedReportForAction;
  AdminUpdateStatusResult? get lastUpdatedResult => _lastUpdatedResult;

  List<ReportModel> get filteredReports {
    var list = _adminReports;
    if (_selectedTab != 'Semua') {
      list = list.where((r) => r.status.toLowerCase() == _selectedTab.toLowerCase()).toList();
    }
    if (_selectedCategory != 'Semua') {
      if (_selectedCategory == 'Lampu / AC') {
        list = list.where((r) => r.kategori.toLowerCase().contains('lampu') || r.kategori.toLowerCase().contains('ac')).toList();
      } else if (_selectedCategory == 'DLL') {
        final mainKats = ['kursi', 'proyektor', 'lampu', 'ac'];
        list = list.where((r) => !mainKats.any((k) => r.kategori.toLowerCase().contains(k))).toList();
      } else {
        list = list.where((r) => r.kategori.toLowerCase() == _selectedCategory.toLowerCase()).toList();
      }
    }
    return list;
  }

  void setSelectedTab(String tab) {
    _selectedTab = tab;
    notifyListeners();
  }

  void setSelectedCategory(String category) {
    _selectedCategory = category;
    notifyListeners();
  }

  void clearCategoryFilter() {
    _selectedCategory = 'Semua';
    notifyListeners();
  }

  void selectReportForAction(ReportModel report) {
    _selectedReportForAction = report;
    notifyListeners();
  }

  Future<void> fetchSummary() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final res = await _adminService.getDashboardSummary();
      _summary = res;
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _isLoading = false;
      _error = e.toString().replaceAll('Exception: ', '');
      notifyListeners();
    }
  }

  Future<void> fetchReports({String? filter}) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final res = await _adminService.getAdminReports(statusFilter: filter);
      _adminReports = res['laporan'];
      _totalLaporan = res['total_laporan'];
      _menungguPeninjauan = res['menunggu_peninjauan'];
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _isLoading = false;
      _error = e.toString().replaceAll('Exception: ', '');
      notifyListeners();
    }
  }

  Future<bool> updateReportStatus({
    required String idLaporan,
    required String status,
    String? aksiTeknis,
    String? catatan,
    String? alasanPenolakan,
    String adminId = 'USR-002',
    String adminName = 'Administrator Fasilitas',
  }) async {
    _isUpdating = true;
    _error = null;
    notifyListeners();

    try {
      final res = await _adminService.updateReportStatus(
        idLaporan: idLaporan,
        status: status,
        aksiTeknis: aksiTeknis,
        catatan: catatan,
        alasanPenolakan: alasanPenolakan,
        adminId: adminId,
        adminName: adminName,
      );
      _lastUpdatedResult = res;
      _isUpdating = false;

      // Perbarui status secara lokal di memori
      for (var r in _adminReports) {
        if (r.idLaporan == idLaporan || r.nomorTiket == idLaporan) {
          // Refresh data list
          fetchReports();
          fetchSummary();
          break;
        }
      }

      notifyListeners();
      return true;
    } catch (e) {
      _isUpdating = false;
      _error = e.toString().replaceAll('Exception: ', '');
      notifyListeners();
      return false;
    }
  }
}
