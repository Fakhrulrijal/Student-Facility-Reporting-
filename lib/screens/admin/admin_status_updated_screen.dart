import 'package:flutter/material.dart';
import '../../models/admin_model.dart';
import 'admin_navigation_shell.dart';

class AdminStatusUpdatedScreen extends StatelessWidget {
  final AdminUpdateStatusResult result;

  const AdminStatusUpdatedScreen({Key? key, required this.result}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final isRejected = result.statusBaru == 'Ditolak';

    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 28.0, vertical: 24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Spacer(),

              // Success Icon Circle (Slide 23 Mockup)
              Center(
                child: Container(
                  width: 90,
                  height: 90,
                  decoration: BoxDecoration(
                    color: isRejected ? const Color(0xFFFEE2E2) : const Color(0xFFDCFCE7),
                    shape: BoxShape.circle,
                  ),
                  child: Icon(
                    isRejected ? Icons.highlight_off_rounded : Icons.check_rounded,
                    size: 54,
                    color: isRejected ? const Color(0xFFDC2626) : const Color(0xFF16A34A),
                  ),
                ),
              ),
              const SizedBox(height: 24),

              Text(
                isRejected ? 'Laporan Ditolak' : 'Status Diperbarui',
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF1E293B),
                ),
              ),
              const SizedBox(height: 12),

              const Text(
                'Perubahan tersimpan di database dan notifikasi terkirim ke pelapor.',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 14,
                  color: Color(0xFF64748B),
                  height: 1.4,
                ),
              ),
              const SizedBox(height: 20),

              // Transition Badge (Slide 23 Mockup: "Tiket #TK-0012 → Diproses")
              Center(
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF1F5F9),
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: const Color(0xFFCBD5E1)),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        'Tiket ${result.nomorTiket}',
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFF1E3A8A)),
                      ),
                      const SizedBox(width: 8),
                      const Icon(Icons.arrow_forward_rounded, size: 16, color: Colors.grey),
                      const SizedBox(width: 8),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                        decoration: BoxDecoration(
                          color: isRejected ? const Color(0xFFFEE2E2) : const Color(0xFFDBEAFE),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Text(
                          result.statusBaru,
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                            color: isRejected ? const Color(0xFFB91C1C) : const Color(0xFF1D4ED8),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 24),

              // Card Simulasi Push Notification FCM (Slide 23)
              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: const Color(0xFFF8FAFC),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: const Color(0xFFE2E8F0)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.notifications_active_outlined, size: 16, color: Color(0xFF1E3A8A)),
                        const SizedBox(width: 8),
                        const Text(
                          'Pesan Notifikasi ke Pelapor:',
                          style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Color(0xFF64748B)),
                        ),
                      ],
                    ),
                    const SizedBox(height: 6),
                    Text(
                      result.notificationTitle,
                      style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: Color(0xFF1E293B)),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      result.notificationBody,
                      style: TextStyle(fontSize: 12, color: Colors.grey.shade700, height: 1.3),
                    ),
                  ],
                ),
              ),

              const Spacer(),

              // Tombol Kembali ke Kelola Laporan (Slide 23 Mockup)
              SizedBox(
                height: 48,
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.pushAndRemoveUntil(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const AdminNavigationShell(initialIndex: 1),
                      ),
                      (route) => false,
                    );
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF1E3A8A),
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                  ),
                  child: const Text('Kembali ke Kelola Laporan', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                ),
              ),
              const SizedBox(height: 12),

              // Tombol Ke Dashboard (Slide 23 Mockup)
              SizedBox(
                height: 46,
                child: OutlinedButton(
                  onPressed: () {
                    Navigator.pushAndRemoveUntil(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const AdminNavigationShell(initialIndex: 0),
                      ),
                      (route) => false,
                    );
                  },
                  style: OutlinedButton.styleFrom(
                    foregroundColor: const Color(0xFF1E3A8A),
                    side: const BorderSide(color: Color(0xFFCBD5E1)),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                  ),
                  child: const Text('Ke Dashboard', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
