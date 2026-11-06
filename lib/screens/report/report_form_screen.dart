import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/report_provider.dart';
import 'qr_scanner_screen.dart';
import 'review_report_screen.dart';

class ReportFormScreen extends StatefulWidget {
  const ReportFormScreen({Key? key}) : super(key: key);

  @override
  State<ReportFormScreen> createState() => _ReportFormScreenState();
}

class _ReportFormScreenState extends State<ReportFormScreen> {
  final TextEditingController _lokasiController = TextEditingController();
  final TextEditingController _deskripsiController = TextEditingController();

  final List<String> _kategoriList = ['Kursi', 'Meja', 'Proyektor', 'Lainnya'];
  final List<String> _keparahanList = ['Ringan', 'Sedang', 'Berat'];

  late String _selectedKategori;
  late String _selectedKeparahan;
  String? _lokasiError;
  String? _deskripsiError;

  @override
  void initState() {
    super.initState();
    final reportProv = Provider.of<ReportProvider>(context, listen: false);
    _lokasiController.text = reportProv.lokasi.isNotEmpty ? reportProv.lokasi : 'Ruang A002 – Gedung A';
    _deskripsiController.text = reportProv.deskripsi.isNotEmpty
        ? reportProv.deskripsi
        : 'Sandaran kursi patah saat dipakai, berbahaya untuk mahasiswa.';
    _selectedKategori = reportProv.kategori.isNotEmpty ? reportProv.kategori : 'Kursi';
    _selectedKeparahan = reportProv.tingkatKeparahan.isNotEmpty ? reportProv.tingkatKeparahan : 'Sedang';
  }

  @override
  void dispose() {
    _lokasiController.dispose();
    _deskripsiController.dispose();
    super.dispose();
  }

  void _proceedToReview() {
    setState(() {
      _lokasiError = null;
      _deskripsiError = null;
    });

    final lokasi = _lokasiController.text.trim();
    final deskripsi = _deskripsiController.text.trim();

    bool hasError = false;
    if (lokasi.isEmpty) {
      _lokasiError = 'Lokasi ruangan/gedung wajib diisi';
      hasError = true;
    }
    if (deskripsi.isEmpty) {
      _deskripsiError = 'Deskripsi kerusakan wajib diisi';
      hasError = true;
    }

    if (hasError) {
      setState(() {});
      return;
    }

    final reportProv = Provider.of<ReportProvider>(context, listen: false);
    reportProv.setFormFields(
      lokasi: lokasi,
      kategori: _selectedKategori,
      tingkatKeparahan: _selectedKeparahan,
      deskripsi: deskripsi,
    );

    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => const ReviewReportScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    final reportProv = context.watch<ReportProvider>();

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text('Lokasi & Deskripsi', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
        backgroundColor: Colors.white,
        foregroundColor: const Color(0xFF1E3A8A),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Preview Thumbnail Foto (Slide 11)
            Row(
              children: [
                Container(
                  width: 80,
                  height: 80,
                  decoration: BoxDecoration(
                    color: const Color(0xFFF1F5F9),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: const Color(0xFFCBD5E1)),
                  ),
                  child: const Icon(Icons.broken_image, size: 36, color: Color(0xFF64748B)),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Foto Kerusakan',
                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: Color(0xFF1E293B)),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        reportProv.kodeQr != null ? 'Aset: ${reportProv.kodeQr}' : 'Foto terlampir',
                        style: TextStyle(fontSize: 12, color: Colors.grey.shade600),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),

            // Lokasi Fasilitas
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  'Tambah Lokasi',
                  style: TextStyle(fontWeight: FontWeight.w600, fontSize: 14, color: Color(0xFF2D3748)),
                ),
                ActionChip(
                  avatar: const Icon(Icons.qr_code_scanner, size: 14, color: Color(0xFF1E3A8A)),
                  label: const Text('Scan QR', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (_) => const QrScannerScreen()),
                    );
                  },
                ),
              ],
            ),
            const SizedBox(height: 6),
            TextField(
              controller: _lokasiController,
              decoration: InputDecoration(
                hintText: 'Contoh: Ruang A002 – Gedung A',
                errorText: _lokasiError,
                prefixIcon: const Icon(Icons.location_on_outlined, color: Color(0xFF1E3A8A)),
                filled: true,
                fillColor: const Color(0xFFF8FAFC),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
              ),
            ),
            const SizedBox(height: 20),

            // Kategori Fasilitas
            const Text(
              'Kategori Fasilitas',
              style: TextStyle(fontWeight: FontWeight.w600, fontSize: 14, color: Color(0xFF2D3748)),
            ),
            const SizedBox(height: 10),
            Wrap(
              spacing: 10,
              children: _kategoriList.map((kat) {
                final isSelected = _selectedKategori == kat;
                return ChoiceChip(
                  label: Text(kat),
                  selected: isSelected,
                  selectedColor: const Color(0xFF1E3A8A),
                  labelStyle: TextStyle(
                    color: isSelected ? Colors.white : const Color(0xFF334155),
                    fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                  ),
                  onSelected: (selected) {
                    if (selected) setState(() => _selectedKategori = kat);
                  },
                );
              }).toList(),
            ),
            const SizedBox(height: 20),

            // Tingkat Keparahan
            const Text(
              'Tingkat Keparahan',
              style: TextStyle(fontWeight: FontWeight.w600, fontSize: 14, color: Color(0xFF2D3748)),
            ),
            const SizedBox(height: 6),
            Row(
              children: _keparahanList.map((kep) {
                return Expanded(
                  child: RadioListTile<String>(
                    contentPadding: EdgeInsets.zero,
                    dense: true,
                    title: Text(kep, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600)),
                    value: kep,
                    groupValue: _selectedKeparahan,
                    activeColor: const Color(0xFF1E3A8A),
                    onChanged: (val) {
                      if (val != null) setState(() => _selectedKeparahan = val);
                    },
                  ),
                );
              }).toList(),
            ),
            const SizedBox(height: 16),

            // Deskripsi
            const Text(
              'Deskripsi Kerusakan',
              style: TextStyle(fontWeight: FontWeight.w600, fontSize: 14, color: Color(0xFF2D3748)),
            ),
            const SizedBox(height: 6),
            TextField(
              controller: _deskripsiController,
              maxLines: 4,
              decoration: InputDecoration(
                hintText: 'Jelaskan kondisi kerusakan fasilitas...',
                errorText: _deskripsiError,
                filled: true,
                fillColor: const Color(0xFFF8FAFC),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
              ),
            ),
            const SizedBox(height: 32),

            // Tombol Lanjut
            SizedBox(
              height: 48,
              child: ElevatedButton(
                onPressed: _proceedToReview,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF1E3A8A),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
                child: const Text('Lanjut', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
