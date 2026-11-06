import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../models/report_model.dart';
import '../../providers/admin_provider.dart';
import '../../widgets/error_dialog.dart';
import 'admin_status_updated_screen.dart';

class AdminActionPlanScreen extends StatefulWidget {
  final ReportModel report;

  const AdminActionPlanScreen({Key? key, required this.report}) : super(key: key);

  @override
  State<AdminActionPlanScreen> createState() => _AdminActionPlanScreenState();
}

class _AdminActionPlanScreenState extends State<AdminActionPlanScreen> {
  String _selectedAksi = 'Perbaiki'; // 'Perbaiki' atau 'Ganti Baru'
  String _selectedStatus = 'Diproses'; // 'Diproses' atau 'Selesai'
  final TextEditingController _catatanController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _catatanController.text = 'Sandaran akan diperbaiki teknisi pada hari Senin.';
  }

  @override
  void dispose() {
    _catatanController.dispose();
    super.dispose();
  }

  void _submitAction() async {
    final adminProv = Provider.of<AdminProvider>(context, listen: false);

    final success = await adminProv.updateReportStatus(
      idLaporan: widget.report.idLaporan,
      status: _selectedStatus,
      aksiTeknis: _selectedAksi,
      catatan: _catatanController.text.trim(),
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
        title: 'Gagal Memperbarui Status',
        message: adminProv.error ?? 'Terjadi kesalahan sistem saat memperbarui status tiket.',
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
          'Tentukan Tindakan',
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
            // Header Fasilitas & Tiket (Slide 21 Mockup)
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: const Color(0xFFF1F5F9),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Row(
                children: [
                  const Icon(Icons.build_circle_outlined, color: Color(0xFF1E3A8A), size: 22),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      '${r.kategori} - ${r.lokasi} · ${r.nomorTiket}',
                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: Color(0xFF1E293B)),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // Aksi Teknis: Perbaiki vs Ganti Baru (Slide 21 Mockup)
            const Text(
              'Aksi Teknis',
              style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Color(0xFF1E293B)),
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(
                  child: InkWell(
                    onTap: () => setState(() => _selectedAksi = 'Perbaiki'),
                    borderRadius: BorderRadius.circular(10),
                    child: Container(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      decoration: BoxDecoration(
                        color: _selectedAksi == 'Perbaiki' ? const Color(0xFF1E3A8A) : const Color(0xFFF8FAFC),
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(
                          color: _selectedAksi == 'Perbaiki' ? const Color(0xFF1E3A8A) : const Color(0xFFCBD5E1),
                        ),
                      ),
                      child: Center(
                        child: Text(
                          'Perbaiki',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: _selectedAksi == 'Perbaiki' ? Colors.white : const Color(0xFF475569),
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: InkWell(
                    onTap: () => setState(() => _selectedAksi = 'Ganti Baru'),
                    borderRadius: BorderRadius.circular(10),
                    child: Container(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      decoration: BoxDecoration(
                        color: _selectedAksi == 'Ganti Baru' ? const Color(0xFF1E3A8A) : const Color(0xFFF8FAFC),
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(
                          color: _selectedAksi == 'Ganti Baru' ? const Color(0xFF1E3A8A) : const Color(0xFFCBD5E1),
                        ),
                      ),
                      child: Center(
                        child: Text(
                          'Ganti Baru',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: _selectedAksi == 'Ganti Baru' ? Colors.white : const Color(0xFF475569),
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),

            // Status Tiket Dropdown (Slide 21 Mockup: "Diproses ▾")
            const Text(
              'Status Tiket',
              style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Color(0xFF1E293B)),
            ),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14),
              decoration: BoxDecoration(
                color: const Color(0xFFF8FAFC),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: Colors.grey.shade300),
              ),
              child: DropdownButtonHideUnderline(
                child: DropdownButton<String>(
                  value: _selectedStatus,
                  isExpanded: true,
                  items: const [
                    DropdownMenuItem(value: 'Diproses', child: Text('Diproses')),
                    DropdownMenuItem(value: 'Selesai', child: Text('Selesai')),
                  ],
                  onChanged: (val) {
                    if (val != null) setState(() => _selectedStatus = val);
                  },
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Catatan Textarea (Slide 21 Mockup)
            const Text(
              'Catatan Petugas',
              style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Color(0xFF1E293B)),
            ),
            const SizedBox(height: 8),
            TextField(
              controller: _catatanController,
              maxLines: 4,
              decoration: InputDecoration(
                hintText: 'Tuliskan catatan teknis untuk pelapor...',
                filled: true,
                fillColor: const Color(0xFFF8FAFC),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
              ),
            ),
            const SizedBox(height: 36),

            // Tombol Update (Slide 21 Mockup)
            SizedBox(
              height: 48,
              child: ElevatedButton(
                onPressed: adminProv.isUpdating ? null : _submitAction,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF1E3A8A),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
                child: adminProv.isUpdating
                    ? const SizedBox(
                        width: 22,
                        height: 22,
                        child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2.5),
                      )
                    : const Text('Update', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
