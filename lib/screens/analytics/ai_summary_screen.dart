import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/analytics_provider.dart';

class AiSummaryScreen extends StatefulWidget {
  const AiSummaryScreen({Key? key}) : super(key: key);

  @override
  State<AiSummaryScreen> createState() => _AiSummaryScreenState();
}

class _AiSummaryScreenState extends State<AiSummaryScreen> {
  final List<String> _periodeList = ['Oktober 2026', 'November 2026', 'Semua Periode'];
  final List<String> _gedungList = ['Semua Gedung', 'Gedung A', 'Gedung B', 'Gedung C'];
  final List<String> _kategoriList = ['Semua Kategori', 'Kursi', 'Proyektor', 'Lampu / AC', 'Meja', 'Lainnya'];

  @override
  Widget build(BuildContext context) {
    final aiProv = context.watch<AnalyticsProvider>();

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text(
          'Rangkuman AI',
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF0F172A)),
        ),
        backgroundColor: Colors.white,
        elevation: 0,
        centerTitle: true,
      ),
      body: aiProv.isGenerating
          ? _buildLoadingState()
          : !aiProv.hasGenerated
              ? _buildFilterState(aiProv)
              : aiProv.summaryResult != null && aiProv.summaryResult!.found
                  ? _buildSummaryResultState(aiProv)
                  : _buildNotFoundState(aiProv),
    );
  }

  // State Loading saat AI memproses data
  Widget _buildLoadingState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: const Color(0xFF7C3AED).withOpacity(0.1),
              shape: BoxShape.circle,
            ),
            child: const CircularProgressIndicator(color: Color(0xFF7C3AED)),
          ),
          const SizedBox(height: 20),
          const Text(
            'Google Gemini AI sedang menganalisis...',
            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Color(0xFF1E293B)),
          ),
          const SizedBox(height: 6),
          Text(
            'Mengekstrak pola kerusakan dominan dan tren per gedung',
            style: TextStyle(fontSize: 13, color: Colors.grey.shade600),
          ),
        ],
      ),
    );
  }

  // State 1: Form Pengaturan Filter (Slide 24 Mockup)
  Widget _buildFilterState(AnalyticsProvider aiProv) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const Text(
            'Atur filter laporan yang ingin dirangkum.',
            style: TextStyle(fontSize: 14, color: Color(0xFF64748B), fontWeight: FontWeight.w500),
          ),
          const SizedBox(height: 24),

          // Dropdown Periode (Slide 24 Mockup)
          const Text('Periode', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: Color(0xFF1E293B))),
          const SizedBox(height: 8),
          _buildDropdownContainer(
            value: aiProv.selectedPeriode,
            items: _periodeList,
            onChanged: (val) => aiProv.setPeriode(val!),
          ),
          const SizedBox(height: 20),

          // Dropdown Gedung (Slide 24 Mockup)
          const Text('Gedung', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: Color(0xFF1E293B))),
          const SizedBox(height: 8),
          _buildDropdownContainer(
            value: aiProv.selectedGedung,
            items: _gedungList,
            onChanged: (val) => aiProv.setGedung(val!),
          ),
          const SizedBox(height: 20),

          // Dropdown Kategori (Slide 24 Mockup)
          const Text('Kategori', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: Color(0xFF1E293B))),
          const SizedBox(height: 8),
          _buildDropdownContainer(
            value: aiProv.selectedKategori,
            items: _kategoriList,
            onChanged: (val) => aiProv.setKategori(val!),
          ),
          const SizedBox(height: 36),

          // Tombol Generate Rangkuman AI (Slide 24 Mockup)
          SizedBox(
            height: 50,
            child: ElevatedButton.icon(
              onPressed: () => aiProv.generateSummary(),
              icon: const Icon(Icons.auto_awesome, size: 20),
              label: const Text('Generate Rangkuman AI', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF7C3AED),
                foregroundColor: Colors.white,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                elevation: 1,
              ),
            ),
          ),
          const SizedBox(height: 28),

          // Simulasi Uji Skenario: Data Tidak Ditemukan (Slide 24 Mockup)
          Center(
            child: ActionChip(
              avatar: const Icon(Icons.bug_report, size: 16, color: Color(0xFF64748B)),
              label: const Text('Uji skenario: data tidak ditemukan', style: TextStyle(fontSize: 12)),
              onPressed: () => aiProv.simulateDataNotFound(),
            ),
          ),
        ],
      ),
    );
  }

  // State 2: Executive Summary Card (Slide 25 Mockup)
  Widget _buildSummaryResultState(AnalyticsProvider aiProv) {
    final res = aiProv.summaryResult!;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Filter Chip Subtitle (Slide 25 Mockup: "Okt 2026 · Semua Gedung · Semua Kategori")
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
            decoration: BoxDecoration(
              color: const Color(0xFFF1F5F9),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.filter_alt_outlined, size: 16, color: Color(0xFF64748B)),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    res.filterLabel,
                    style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13, color: Color(0xFF334155)),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),

          // Card Rangkuman Eksekutif (Slide 25 Mockup)
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: const Color(0xFFE2E8F0)),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.03),
                  blurRadius: 10,
                  offset: const Offset(0, 4),
                ),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: const Color(0xFF7C3AED).withOpacity(0.1),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: const Icon(Icons.auto_awesome, color: Color(0xFF7C3AED), size: 20),
                    ),
                    const SizedBox(width: 10),
                    const Text(
                      'Rangkuman Eksekutif',
                      style: TextStyle(
                        fontSize: 17,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF0F172A),
                      ),
                    ),
                  ],
                ),
                const Divider(height: 28),

                // Bullet points ekstraksi pola AI
                ...res.bullets.map((bullet) {
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 14.0),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          margin: const EdgeInsets.only(top: 6),
                          width: 6,
                          height: 6,
                          decoration: const BoxDecoration(
                            color: Color(0xFF7C3AED),
                            shape: BoxShape.circle,
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Text(
                            bullet,
                            style: const TextStyle(
                              fontSize: 14,
                              color: Color(0xFF334155),
                              height: 1.4,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ),
                      ],
                    ),
                  );
                }).toList(),

                const SizedBox(height: 8),

                // Rekomendasi Highlight Box (Slide 25 Mockup)
                Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: const Color(0xFFFAF5FF),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: const Color(0xFFE9D5FF)),
                  ),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(Icons.lightbulb_outline, color: Color(0xFF7C3AED), size: 20),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          'Rekomendasi: ${res.rekomendasi}',
                          style: const TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.bold,
                            color: Color(0xFF6B21A8),
                            height: 1.4,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 32),

          // Tombol Atur Ulang Filter (Slide 25 Mockup)
          SizedBox(
            height: 48,
            child: OutlinedButton(
              onPressed: () => aiProv.resetFilter(),
              style: OutlinedButton.styleFrom(
                foregroundColor: const Color(0xFF1E3A8A),
                side: const BorderSide(color: Color(0xFFCBD5E1)),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
              ),
              child: const Text('Atur Ulang Filter', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
            ),
          ),
        ],
      ),
    );
  }

  // State 3: Data Tidak Ditemukan (Slide 26 Mockup)
  Widget _buildNotFoundState(AnalyticsProvider aiProv) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 80,
              height: 80,
              decoration: BoxDecoration(
                color: const Color(0xFFEFF6FF),
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.help_outline_rounded, size: 44, color: Color(0xFF1E3A8A)),
            ),
            const SizedBox(height: 20),
            const Text(
              'Data Tidak Ditemukan',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Color(0xFF0F172A),
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Tidak ada laporan yang sesuai dengan filter yang dipilih.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 14, color: Colors.grey.shade600, height: 1.4),
            ),
            const SizedBox(height: 28),
            SizedBox(
              height: 46,
              child: ElevatedButton(
                onPressed: () => aiProv.resetFilter(),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF1E3A8A),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
                child: const Text('Ubah Filter', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDropdownContainer({
    required String value,
    required List<String> items,
    required ValueChanged<String?> onChanged,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: const Color(0xFFCBD5E1)),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<String>(
          value: value,
          isExpanded: true,
          items: items.map((e) {
            return DropdownMenuItem<String>(
              value: e,
              child: Text(e, style: const TextStyle(fontSize: 14, color: Color(0xFF1E293B))),
            );
          }).toList(),
          onChanged: onChanged,
        ),
      ),
    );
  }
}
