import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../providers/report_provider.dart';
import '../../widgets/error_dialog.dart';
import 'report_success_screen.dart';

class ReviewReportScreen extends StatelessWidget {
  const ReviewReportScreen({Key? key}) : super(key: key);

  void _submit(BuildContext context) async {
    final auth = Provider.of<AuthProvider>(context, listen: false);
    final reportProv = Provider.of<ReportProvider>(context, listen: false);

    final success = await reportProv.submitReport(token: auth.token);

    if (success && context.mounted) {
      Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (_) => const ReportSuccessScreen()),
        (route) => route.isFirst,
      );
    } else if (context.mounted) {
      ErrorDialog.show(
        context,
        title: 'Pengiriman Gagal',
        message: reportProv.submitError ?? 'Terjadi kendala saat mengirimkan laporan ke server.',
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final reportProv = context.watch<ReportProvider>();

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text('Tinjau Laporan', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
        backgroundColor: Colors.white,
        foregroundColor: const Color(0xFF1E3A8A),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Preview Card Kerusakan (Slide 12)
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: const Color(0xFFF8FAFC),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: const Color(0xFFE2E8F0)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Lokasi Fasilitas', style: TextStyle(fontSize: 12, color: Colors.grey)),
                  const SizedBox(height: 2),
                  Text(
                    reportProv.lokasi,
                    style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFF1E293B)),
                  ),
                  const Divider(height: 24),

                  const Text('Kategori Kerusakan', style: TextStyle(fontSize: 12, color: Colors.grey)),
                  const SizedBox(height: 2),
                  Text(
                    reportProv.kategori,
                    style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600, color: Color(0xFF1E293B)),
                  ),
                  const Divider(height: 24),

                  const Text('Tingkat Keparahan', style: TextStyle(fontSize: 12, color: Colors.grey)),
                  const SizedBox(height: 4),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: const Color(0xFFFEF3C7),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      reportProv.tingkatKeparahan,
                      style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: Color(0xFFB45309)),
                    ),
                  ),
                  const Divider(height: 24),

                  const Text('Deskripsi Kerusakan', style: TextStyle(fontSize: 12, color: Colors.grey)),
                  const SizedBox(height: 4),
                  Text(
                    reportProv.deskripsi,
                    style: const TextStyle(fontSize: 14, color: Color(0xFF334155), height: 1.4),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Banner Konfirmasi (Slide 12)
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: const Color(0xFFEFF6FF),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: const Color(0xFFBFDBFE)),
              ),
              child: Row(
                children: const [
                  Icon(Icons.info_outline, color: Color(0xFF1E3A8A), size: 20),
                  SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      'Periksa kembali data laporan sebelum dikirim.',
                      style: TextStyle(fontSize: 13, color: Color(0xFF1E3A8A), fontWeight: FontWeight.w500),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 36),

            // Tombol Kirim Laporan & Revisi
            SizedBox(
              height: 48,
              child: ElevatedButton(
                onPressed: reportProv.isSubmitting ? null : () => _submit(context),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF1E3A8A),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
                child: reportProv.isSubmitting
                    ? const SizedBox(
                        width: 22,
                        height: 22,
                        child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2.5),
                      )
                    : const Text('Kirim Laporan', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ),
            ),
            const SizedBox(height: 12),
            SizedBox(
              height: 46,
              child: OutlinedButton(
                onPressed: () => Navigator.pop(context),
                style: OutlinedButton.styleFrom(
                  foregroundColor: const Color(0xFF1E3A8A),
                  side: const BorderSide(color: Color(0xFFCBD5E1)),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
                child: const Text('Revisi / Edit', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
