import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/admin_provider.dart';
import '../../providers/auth_provider.dart';
import '../auth/login_screen.dart';
import 'admin_manage_reports_screen.dart';

class AdminDashboardScreen extends StatefulWidget {
  final Function(int)? onNavigateTab;

  const AdminDashboardScreen({Key? key, this.onNavigateTab}) : super(key: key);

  @override
  State<AdminDashboardScreen> createState() => _AdminDashboardScreenState();
}

class _AdminDashboardScreenState extends State<AdminDashboardScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      Provider.of<AdminProvider>(context, listen: false).fetchSummary();
    });
  }

  @override
  Widget build(BuildContext context) {
    final adminProv = context.watch<AdminProvider>();
    final auth = context.watch<AuthProvider>();
    final summary = adminProv.summary;

    final total = summary?.totalLaporan ?? 34;
    final diproses = summary?.diproses ?? 8;
    final selesai = summary?.selesai ?? 21;
    final breakdown = summary?.breakdownKategori ?? {
      'Kursi': 12,
      'Proyektor': 7,
      'Lampu / AC': 6,
      'DLL': 9,
    };

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text(
          'Dashboard Admin',
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF0F172A)),
        ),
        backgroundColor: Colors.white,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh_rounded, color: Color(0xFF1E3A8A)),
            tooltip: 'Refresh Data',
            onPressed: () {
              adminProv.fetchSummary();
            },
          ),
          IconButton(
            icon: const Icon(Icons.logout_rounded, color: Colors.redAccent),
            tooltip: 'Logout',
            onPressed: () {
              auth.logout();
              Navigator.pushAndRemoveUntil(
                context,
                MaterialPageRoute(builder: (_) => const LoginScreen()),
                (route) => false,
              );
            },
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () async {
          await adminProv.fetchSummary();
        },
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Summary Metrics Row (Slide 18 Mockup)
              Row(
                children: [
                  Expanded(
                    child: _buildMetricCard(
                      value: diproses.toString(),
                      label: 'Diproses',
                      bgColor: const Color(0xFFEFF6FF),
                      textColor: const Color(0xFF1D4ED8),
                      borderColor: const Color(0xFFBFDBFE),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: _buildMetricCard(
                      value: selesai.toString(),
                      label: 'Selesai',
                      bgColor: const Color(0xFFF0FDF4),
                      textColor: const Color(0xFF15803D),
                      borderColor: const Color(0xFFBBF7D0),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: _buildMetricCard(
                      value: total.toString(),
                      label: 'Total',
                      bgColor: const Color(0xFF1E3A8A),
                      textColor: Colors.white,
                      borderColor: const Color(0xFF1E3A8A),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),

              // Breakdown Kategori Kerusakan (Slide 18 Mockup)
              const Text(
                'Kategori Kerusakan',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF0F172A),
                ),
              ),
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: const Color(0xFFE2E8F0)),
                ),
                child: Column(
                  children: [
                    _buildCategoryRow('Kursi', breakdown['Kursi'] ?? 12, Icons.chair_outlined, Colors.blue),
                    const Divider(height: 18),
                    _buildCategoryRow('Proyektor', breakdown['Proyektor'] ?? 7, Icons.videocam_outlined, Colors.purple),
                    const Divider(height: 18),
                    _buildCategoryRow('Lampu / AC', breakdown['Lampu / AC'] ?? 6, Icons.lightbulb_outline, Colors.amber.shade800),
                    const Divider(height: 18),
                    _buildCategoryRow('DLL', breakdown['DLL'] ?? 9, Icons.category_outlined, Colors.teal),
                  ],
                ),
              ),
              const SizedBox(height: 28),

              // Action Cards (Slide 18 Mockup)
              _buildActionCard(
                title: 'Kelola Laporan',
                subtitle: 'Evaluasi, terima, atau tolak laporan civitas akademika',
                icon: Icons.assignment_outlined,
                color: const Color(0xFF1E3A8A),
                onTap: () {
                  if (widget.onNavigateTab != null) {
                    widget.onNavigateTab!(1);
                  } else {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (_) => const AdminManageReportsScreen()),
                    );
                  }
                },
              ),
              const SizedBox(height: 12),
              _buildActionCard(
                title: 'Rangkuman AI',
                subtitle: 'Ringkasan eksekutif dan tren kerusakan berbasis AI',
                icon: Icons.auto_awesome,
                color: const Color(0xFF7C3AED),
                onTap: () {
                  if (widget.onNavigateTab != null) {
                    widget.onNavigateTab!(2);
                  }
                },
              ),
              const SizedBox(height: 12),
              _buildActionCard(
                title: 'Prioritas Penanganan',
                subtitle: 'Scoring urgensi penanganan perbaikan fasilitas',
                icon: Icons.format_list_numbered_rounded,
                color: const Color(0xFFD97706),
                onTap: () {
                  if (widget.onNavigateTab != null) {
                    widget.onNavigateTab!(3);
                  }
                },
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMetricCard({
    required String value,
    required String label,
    required Color bgColor,
    required Color textColor,
    required Color borderColor,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 18, horizontal: 12),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: borderColor),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.02),
            blurRadius: 4,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        children: [
          Text(
            value,
            style: TextStyle(
              fontSize: 26,
              fontWeight: FontWeight.bold,
              color: textColor,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            label,
            style: TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w600,
              color: textColor.withOpacity(0.9),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCategoryRow(String name, int count, IconData icon, Color color) {
    return Row(
      children: [
        Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: color.withOpacity(0.1),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Icon(icon, color: color, size: 20),
        ),
        const SizedBox(width: 14),
        Expanded(
          child: Text(
            name,
            style: const TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.w600,
              color: Color(0xFF1E293B),
            ),
          ),
        ),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
          decoration: BoxDecoration(
            color: const Color(0xFFF1F5F9),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Text(
            count.toString(),
            style: const TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.bold,
              color: Color(0xFF334155),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildActionCard({
    required String title,
    required String subtitle,
    required IconData icon,
    required Color color,
    required VoidCallback onTap,
  }) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(14),
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: const Color(0xFFE2E8F0)),
        ),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: color.withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(icon, color: color, size: 24),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF0F172A),
                    ),
                  ),
                  const SizedBox(height: 3),
                  Text(
                    subtitle,
                    style: TextStyle(fontSize: 12, color: Colors.grey.shade600),
                  ),
                ],
              ),
            ),
            const Icon(Icons.arrow_forward_ios_rounded, size: 16, color: Colors.grey),
          ],
        ),
      ),
    );
  }
}
