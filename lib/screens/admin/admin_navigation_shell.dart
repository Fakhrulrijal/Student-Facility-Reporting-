import 'package:flutter/material.dart';
import 'admin_dashboard_screen.dart';
import 'admin_manage_reports_screen.dart';
import '../analytics/ai_summary_screen.dart';

class AdminNavigationShell extends StatefulWidget {
  final int initialIndex;

  const AdminNavigationShell({Key? key, this.initialIndex = 0}) : super(key: key);

  @override
  State<AdminNavigationShell> createState() => _AdminNavigationShellState();
}

class _AdminNavigationShellState extends State<AdminNavigationShell> {
  late int _currentIndex;

  @override
  void initState() {
    super.initState();
    _currentIndex = widget.initialIndex;
  }

  void _onNavigate(int index) {
    setState(() {
      _currentIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    final List<Widget> pages = [
      AdminDashboardScreen(onNavigateTab: _onNavigate),
      const AdminManageReportsScreen(),
      const AiSummaryScreen(),
      _buildPlaceholderScreen('Prioritas Penanganan AI', 'Modul 6 (MOD-06) - Engine Scoring & Ranking Prioritas AI'),
    ];

    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: pages,
      ),
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          border: Border(top: BorderSide(color: Colors.grey.shade200)),
        ),
        child: BottomNavigationBar(
          currentIndex: _currentIndex,
          backgroundColor: Colors.white,
          selectedItemColor: const Color(0xFF1E3A8A),
          unselectedItemColor: const Color(0xFF94A3B8),
          type: BottomNavigationBarType.fixed,
          selectedLabelStyle: const TextStyle(fontWeight: FontWeight.bold, fontSize: 11),
          unselectedLabelStyle: const TextStyle(fontSize: 11),
          elevation: 0,
          onTap: _onNavigate,
          items: const [
            BottomNavigationBarItem(
              icon: Icon(Icons.dashboard_outlined),
              activeIcon: Icon(Icons.dashboard_rounded),
              label: 'Dashboard',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.assignment_outlined),
              activeIcon: Icon(Icons.assignment_rounded),
              label: 'Laporan',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.auto_awesome_outlined),
              activeIcon: Icon(Icons.auto_awesome),
              label: 'Rangkum',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.format_list_numbered_outlined),
              activeIcon: Icon(Icons.format_list_numbered_rounded),
              label: 'Prioritas',
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPlaceholderScreen(String title, String subtitle) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF0F172A))),
        backgroundColor: Colors.white,
        elevation: 0,
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(32.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                padding: const EdgeInsets.all(18),
                decoration: BoxDecoration(
                  color: const Color(0xFFEFF6FF),
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.engineering_outlined, size: 48, color: Color(0xFF1E3A8A)),
              ),
              const SizedBox(height: 20),
              Text(
                title,
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFF1E293B)),
              ),
              const SizedBox(height: 8),
              Text(
                subtitle,
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 13, color: Colors.grey.shade600, height: 1.4),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
