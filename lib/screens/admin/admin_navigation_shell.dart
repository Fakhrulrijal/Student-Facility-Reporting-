import 'package:flutter/material.dart';
import 'admin_dashboard_screen.dart';
import 'admin_manage_reports_screen.dart';
import '../analytics/ai_summary_screen.dart';
import 'admin_priority_screen.dart';

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
      const AdminPriorityScreen(),
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
}
