import 'package:flutter/material.dart';
import '../models/priority_model.dart';
import '../services/priority_service.dart';

class PriorityProvider with ChangeNotifier {
  final PriorityService _service = PriorityService();

  List<PrioritizedTicketModel> _tickets = [];
  PrioritySummaryModel? _summary;
  bool _isLoading = false;
  bool _isRecalculating = false;
  String? _errorMessage;

  String _selectedPriorityFilter = 'Semua';
  String _selectedStatusFilter = 'Semua';
  String _selectedGedungFilter = 'Semua Gedung';

  List<PrioritizedTicketModel> get tickets => _tickets;
  PrioritySummaryModel? get summary => _summary;
  bool get isLoading => _isLoading;
  bool get isRecalculating => _isRecalculating;
  String? get errorMessage => _errorMessage;

  String get selectedPriorityFilter => _selectedPriorityFilter;
  String get selectedStatusFilter => _selectedStatusFilter;
  String get selectedGedungFilter => _selectedGedungFilter;

  // Memuat data perangkingan tiket prioritas
  Future<void> fetchPrioritizedTickets() async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final res = await _service.fetchPrioritizedTickets(
        status: _selectedStatusFilter,
        prioritas: _selectedPriorityFilter,
        gedung: _selectedGedungFilter,
      );
      _summary = res['summary'];
      _tickets = res['tickets'];
    } catch (e) {
      _errorMessage = e.toString().replaceAll('Exception: ', '');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Memicu kalkulasi ulang berbasis AI Google Gemini / Heuristik
  Future<bool> recalculatePriorities() async {
    _isRecalculating = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final res = await _service.recalculatePriorities(
        status: _selectedStatusFilter,
        prioritas: _selectedPriorityFilter,
        gedung: _selectedGedungFilter,
      );
      _summary = res['summary'];
      _tickets = res['tickets'];
      _isRecalculating = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = e.toString().replaceAll('Exception: ', '');
      _isRecalculating = false;
      notifyListeners();
      return false;
    }
  }

  void setPriorityFilter(String filter) {
    if (_selectedPriorityFilter != filter) {
      _selectedPriorityFilter = filter;
      fetchPrioritizedTickets();
    }
  }

  void setStatusFilter(String filter) {
    if (_selectedStatusFilter != filter) {
      _selectedStatusFilter = filter;
      fetchPrioritizedTickets();
    }
  }

  void setGedungFilter(String filter) {
    if (_selectedGedungFilter != filter) {
      _selectedGedungFilter = filter;
      fetchPrioritizedTickets();
    }
  }
}
