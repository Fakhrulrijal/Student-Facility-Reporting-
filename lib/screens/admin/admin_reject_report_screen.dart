import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../models/report_model.dart';
import '../../providers/admin_provider.dart';
import '../../widgets/error_dialog.dart';
import 'admin_status_updated_screen.dart';

class AdminRejectReportScreen extends StatefulWidget {
  final ReportModel report;

  const AdminRejectReportScreen({Key? key, required this.report}) : super(key: key);

  @override
  State<AdminRejectReportScreen> createState() => _AdminRejectReportScreenState();
}

class _AdminRejectReportScreenState extends State<AdminRejectReportScreen> {
  final TextEditingController _alasanController = TextEditingController();
  String? _alasanError;

  @override
  void initState() {
    super.initState();
    _alasanController.text = 'Laporan duplikat — kerusakan yang sama sudah dilaporkan pada tiket #TK-0009.';
  }

  @override
  void dispose() {
    _alasanController.dispose();
    super.dispose();
  }

  void _submitRejection() async {
    final alasan = _alasanController.text.trim();
    if (alasan.isEmpty) {
      setState(() {
        _alasanError = 'Alasan penolakan wajib diisi.';
      });
      return;
    }

    final adminProv = Provider.of<AdminProvider>(context, listen: false);

    final success = await adminProv.updateReportStatus(
      idLaporan: widget.report.idLaporan,
      status: 'Ditolak',
      alasanPenolakan: alasan,
    );

    if (success && mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => AdminStatusUpdatedScreen(
            result: adminProv.lastUpdatedResult!,
          ),
        ),
      );
    } else if (mounted) {
      ErrorDialog.show(
        context,
        title: 'Penolakan Gagal',
        message: adminProv.error ?? 'Terjadi kesalahan sistem saat memproses penolakan laporan.',
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final adminProv = context.watch<AdminProvider>();
    final r = widget.report;

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text(
          'Tolak Laporan',
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF0F172A)),
        ),
        backgroundColor: Colors.white,
        foregroundColor: const Color(0xFF1E3A8A),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Header Fasilitas & Tiket (Slide 22 Mockup)
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: const Color(0xFFFEF2F2),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: Colors.red.shade200),
              ),
              child: Row(
                children: [
                  const Icon(Icons.cancel_outlined, color: Colors.red, size: 22),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      '${r.kategori} - ${r.lokasi} · ${r.nomorTiket}',
                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: Color(0xFF991B1B)),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // Alasan Penolakan Textarea (Slide 22 Mockup)
            const Text(
              'Alasan Penolakan (wajib)',
              style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Color(0xFF1E293B)),
            ),
            const SizedBox(height: 8),
            TextField(
              controller: _alasanController,
              maxLines: 4,
              onChanged: (_) {
                if (_alasanError != null) setState(() => _alasanError = null);
              },
              decoration: InputDecoration(
                hintText: 'Tuliskan alasan mengapa laporan tidak layak diproses...',
                errorText: _alasanError,
                filled: true,
                fillColor: const Color(0xFFF8FAFC),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
              ),
            ),
            const SizedBox(height: 16),

            // Info Banner Notifikasi (Slide 22 Mockup)
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
                      'Pelapor akan menerima notifikasi beserta alasan ini.',
                      style: TextStyle(fontSize: 13, color: Color(0xFF1E3A8A), fontWeight: FontWeight.w500),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 36),

            // Tombol Tolak & Kirim Catatan (Slide 22 Mockup)
            SizedBox(
              height: 48,
              child: ElevatedButton(
                onPressed: adminProv.isUpdating ? null : _submitRejection,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFFDC2626),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
                child: adminProv.isUpdating
                    ? const SizedBox(
                        width: 22,
                        height: 22,
                        child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2.5),
                      )
                    : const Text(
                        'Tolak & Kirim Catatan',
                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                      ),
              ),
            ),
            const SizedBox(height: 12),

            // Tombol Batal
            SizedBox(
              height: 46,
              child: OutlinedButton(
                onPressed: () => Navigator.pop(context),
                style: OutlinedButton.styleFrom(
                  foregroundColor: Colors.grey.shade700,
                  side: const BorderSide(color: Color(0xFFCBD5E1)),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
                child: const Text('Batal', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
