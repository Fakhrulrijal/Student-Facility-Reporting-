import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../models/priority_model.dart';
import '../../models/report_model.dart';
import '../../providers/priority_provider.dart';
import 'admin_report_detail_screen.dart';

class AdminPriorityScreen extends StatefulWidget {
  const AdminPriorityScreen({Key? key}) : super(key: key);

  @override
  State<AdminPriorityScreen> createState() => _AdminPriorityScreenState();
}

class _AdminPriorityScreenState extends State<AdminPriorityScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      Provider.of<PriorityProvider>(context, listen: false).fetchPrioritizedTickets();
    });
  }

  Color _getPriorityColor(String prioritas) {
    switch (prioritas.toLowerCase()) {
      case 'tinggi':
        return const Color(0xFFDC2626); // Merah tegas
      case 'sedang':
        return const Color(0xFFD97706); // Amber/Oranye tegas
      case 'rendah':
        return const Color(0xFF16A34A); // Hijau
      default:
        return const Color(0xFF2563EB); // Biru
    }
  }

  Color _getPriorityBgColor(String prioritas) {
    switch (prioritas.toLowerCase()) {
      case 'tinggi':
        return const Color(0xFFFEF2F2);
      case 'sedang':
        return const Color(0xFFFFFBEB);
      case 'rendah':
        return const Color(0xFFF0FDF4);
      default:
        return const Color(0xFFEFF6FF);
    }
  }

  void _showScoreDetailSheet(BuildContext context, PrioritizedTicketModel item) {
    final bd = item.breakdown;
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (ctx) {
        return Padding(
          padding: EdgeInsets.only(
            left: 24,
            right: 24,
            top: 24,
            bottom: MediaQuery.of(ctx).viewInsets.bottom + 32,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Center(
                child: Container(
                  width: 48,
                  height: 4,
                  decoration: BoxDecoration(
                    color: Colors.grey.shade300,
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ),
              const SizedBox(height: 18),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Rincian Skor Urgensi AI',
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF0F172A)),
                      ),
                      Text(
                        '${item.nomorTiket} · Rank #${item.rank}',
                        style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                      ),
                    ],
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                    decoration: BoxDecoration(
                      color: _getPriorityBgColor(item.kategoriPrioritas),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: _getPriorityColor(item.kategoriPrioritas).withValues(alpha: 0.3)),
                    ),
                    child: Text(
                      '${item.skorUrgensi} / 100',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 18,
                        color: _getPriorityColor(item.kategoriPrioritas),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 20),

              // Formula Card
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: const Color(0xFFF8FAFC),
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: const Color(0xFFE2E8F0)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text(
                      'FORMULA KOMPOSIT SKOR URGENSI',
                      style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11, color: Color(0xFF64748B)),
                    ),
                    SizedBox(height: 4),
                    Text(
                      'Skor = (0.40 × Keparahan) + (0.30 × Frekuensi) + (0.30 × Dampak)',
                      style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: Color(0xFF1E293B)),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 16),

              // 1. Keparahan Laporan (40%)
              _buildVariableTile(
                title: '1. Keparahan Laporan (Bobot 40%)',
                subTitle: 'Kondisi: ${item.tingkatKeparahan} (Nilai: ${bd.keparahanNilai.toInt()})',
                subskorText: '+${bd.keparahanSubskor.toStringAsFixed(1)} pts',
                progress: bd.keparahanNilai / 100,
                color: const Color(0xFFEF4444),
              ),
              const SizedBox(height: 12),

              // 2. Frekuensi Kerusakan (30%)
              _buildVariableTile(
                title: '2. Frekuensi Kerusakan (Bobot 30%)',
                subTitle: '${bd.frekuensiCount} laporan terkait aset/gedung sama (Nilai: ${bd.frekuensiNilai.toInt()})',
                subskorText: '+${bd.frekuensiSubskor.toStringAsFixed(1)} pts',
                progress: bd.frekuensiNilai / 100,
                color: const Color(0xFFF59E0B),
              ),
              const SizedBox(height: 12),

              // 3. Dampak Fasilitas (30%)
              _buildVariableTile(
                title: '3. Dampak Fasilitas (Bobot 30%)',
                subTitle: bd.dampakKeterangan,
                subskorText: '+${bd.dampakSubskor.toStringAsFixed(1)} pts',
                progress: bd.dampakNilai / 100,
                color: const Color(0xFF3B82F6),
              ),
              const SizedBox(height: 20),

              // Rekomendasi AI Box
              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: const Color(0xFFEFF6FF),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: const Color(0xFFBFDBFE)),
                ),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(Icons.auto_awesome, color: Color(0xFF1E3A8A), size: 20),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Rekomendasi Operasional AI:',
                            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFF1E3A8A)),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            item.rekomendasiTindakan,
                            style: const TextStyle(fontSize: 12.5, color: Color(0xFF1E293B)),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              SizedBox(
                height: 46,
                child: ElevatedButton(
                  onPressed: () => Navigator.pop(ctx),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF1E3A8A),
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                  ),
                  child: const Text('Tutup', style: TextStyle(fontWeight: FontWeight.bold)),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  static Widget _buildVariableTile({
    required String title,
    required String subTitle,
    required String subskorText,
    required double progress,
    required Color color,
  }) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: Colors.grey.shade200),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                title,
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFF0F172A)),
              ),
              Text(
                subskorText,
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: color),
              ),
            ],
          ),
          const SizedBox(height: 4),
          Text(
            subTitle,
            style: TextStyle(fontSize: 11.5, color: Colors.grey.shade600),
          ),
          const SizedBox(height: 8),
          ClipRRect(
            borderRadius: BorderRadius.circular(4),
            child: LinearProgressIndicator(
              value: progress.clamp(0.0, 1.0),
              backgroundColor: Colors.grey.shade100,
              valueColor: AlwaysStoppedAnimation<Color>(color),
              minHeight: 6,
            ),
          ),
        ],
      ),
    );
  }

  void _openReportDetail(BuildContext context, PrioritizedTicketModel item) {
    final report = ReportModel(
      idLaporan: item.idLaporan,
      nomorTiket: item.nomorTiket,
      idUser: item.idUser,
      namaPelapor: item.namaPelapor,
      nomorIndukPelapor: item.nomorIndukPelapor,
      idFasilitas: null,
      kodeQr: item.kodeQr,
      lokasi: item.lokasi,
      kategori: item.kategori,
      tingkatKeparahan: item.tingkatKeparahan,
      deskripsi: 'Evaluasi Skor AI: ${item.skorUrgensi}/100 (${item.kategoriPrioritas}). ${item.rekomendasiTindakan}',
      fotoUrl: item.fotoUrl,
      status: item.status,
      createdAt: item.createdAt,
    );

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => AdminReportDetailScreen(report: report),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<PriorityProvider>();
    final summary = provider.summary;

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text(
          'Prioritas Penanganan AI',
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF0F172A)),
        ),
        backgroundColor: Colors.white,
        elevation: 0,
        actions: [
          IconButton(
            icon: provider.isRecalculating
                ? const SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(strokeWidth: 2, color: Color(0xFF1E3A8A)),
                  )
                : const Icon(Icons.sync_rounded, color: Color(0xFF1E3A8A)),
            tooltip: 'Hitung Ulang Prioritas AI',
            onPressed: provider.isRecalculating ? null : () => provider.recalculatePriorities(),
          ),
        ],
      ),
      body: provider.isLoading
          ? const Center(child: CircularProgressIndicator(color: Color(0xFF1E3A8A)))
          : RefreshIndicator(
              onRefresh: () async => provider.fetchPrioritizedTickets(),
              child: SingleChildScrollView(
                physics: const AlwaysScrollableScrollPhysics(),
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // Banner Engine AI
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          colors: [Color(0xFF1E3A8A), Color(0xFF2563EB)],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                        borderRadius: BorderRadius.circular(16),
                        boxShadow: [
                          BoxShadow(
                            color: const Color(0xFF1E3A8A).withValues(alpha: 0.25),
                            blurRadius: 10,
                            offset: const Offset(0, 4),
                          ),
                        ],
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Row(
                                children: const [
                                  Icon(Icons.auto_awesome, color: Colors.amberAccent, size: 20),
                                  SizedBox(width: 8),
                                  Text(
                                    'AI Scoring Engine v1.0',
                                    style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14),
                                  ),
                                ],
                              ),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                                decoration: BoxDecoration(
                                  color: Colors.white.withValues(alpha: 0.2),
                                  borderRadius: BorderRadius.circular(20),
                                ),
                                child: const Text(
                                  'Gemini & Composite',
                                  style: TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w600),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 10),
                          const Text(
                            'Kalkulasi otomatis skor urgensi 0-100 berbasis Keparahan (40%), Frekuensi Kerusakan (30%), dan Dampak Fasilitas (30%).',
                            style: TextStyle(color: Colors.white70, fontSize: 12.5, height: 1.4),
                          ),
                          const SizedBox(height: 12),
                          SizedBox(
                            height: 36,
                            child: ElevatedButton.icon(
                              onPressed: provider.isRecalculating ? null : () => provider.recalculatePriorities(),
                              icon: provider.isRecalculating
                                  ? const SizedBox(
                                      width: 14,
                                      height: 14,
                                      child: CircularProgressIndicator(color: Color(0xFF1E3A8A), strokeWidth: 2),
                                    )
                                  : const Icon(Icons.flash_on_rounded, size: 16),
                              label: Text(
                                provider.isRecalculating ? 'Mengkalkulasi...' : 'Kalkulasi Ulang Prioritas',
                                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12),
                              ),
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.white,
                                foregroundColor: const Color(0xFF1E3A8A),
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                                elevation: 0,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),

                    // KPI Metrik Prioritas
                    if (summary != null)
                      Row(
                        children: [
                          Expanded(
                            child: _buildKpiCard(
                              label: 'Tinggi (>80)',
                              value: summary.totalTinggi.toString(),
                              color: const Color(0xFFDC2626),
                              bgColor: const Color(0xFFFEF2F2),
                            ),
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: _buildKpiCard(
                              label: 'Sedang (50-80)',
                              value: summary.totalSedang.toString(),
                              color: const Color(0xFFD97706),
                              bgColor: const Color(0xFFFFFBEB),
                            ),
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: _buildKpiCard(
                              label: 'Rendah (<50)',
                              value: summary.totalRendah.toString(),
                              color: const Color(0xFF16A34A),
                              bgColor: const Color(0xFFF0FDF4),
                            ),
                          ),
                        ],
                      ),
                    const SizedBox(height: 16),

                    // Filter Chip Prioritas
                    SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: ['Semua', 'Tinggi', 'Sedang', 'Rendah'].map((filter) {
                          final isSelected = provider.selectedPriorityFilter == filter;
                          return Padding(
                            padding: const EdgeInsets.only(right: 8.0),
                            child: FilterChip(
                              label: Text(filter == 'Semua' ? 'Semua Prioritas' : 'Prioritas $filter'),
                              selected: isSelected,
                              onSelected: (_) => provider.setPriorityFilter(filter),
                              selectedColor: const Color(0xFF1E3A8A),
                              labelStyle: TextStyle(
                                color: isSelected ? Colors.white : const Color(0xFF475569),
                                fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                                fontSize: 12,
                              ),
                              backgroundColor: Colors.white,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(20),
                                side: BorderSide(
                                  color: isSelected ? const Color(0xFF1E3A8A) : Colors.grey.shade300,
                                ),
                              ),
                            ),
                          );
                        }).toList(),
                      ),
                    ),
                    const SizedBox(height: 14),

                    // Daftar Tiket Terurut Ranking
                    if (provider.tickets.isEmpty)
                      Container(
                        padding: const EdgeInsets.all(32),
                        alignment: Alignment.center,
                        child: Column(
                          children: [
                            Icon(Icons.inbox_outlined, size: 48, color: Colors.grey.shade400),
                            const SizedBox(height: 12),
                            Text(
                              'Tidak ada tiket pada kategori prioritas ini.',
                              style: TextStyle(color: Colors.grey.shade600, fontSize: 14),
                            ),
                          ],
                        ),
                      )
                    else
                      ListView.separated(
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        itemCount: provider.tickets.length,
                        separatorBuilder: (_, __) => const SizedBox(height: 12),
                        itemBuilder: (ctx, idx) {
                          final item = provider.tickets[idx];
                          final pColor = _getPriorityColor(item.kategoriPrioritas);
                          final pBgColor = _getPriorityBgColor(item.kategoriPrioritas);

                          return Container(
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(16),
                              border: Border.all(
                                color: idx == 0
                                    ? const Color(0xFFDC2626).withValues(alpha: 0.4)
                                    : Colors.grey.shade200,
                                width: idx == 0 ? 1.5 : 1,
                              ),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withValues(alpha: 0.03),
                                  blurRadius: 6,
                                  offset: const Offset(0, 2),
                                ),
                              ],
                            ),
                            child: Padding(
                              padding: const EdgeInsets.all(16.0),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  // Baris Header: Rank & Badge Skor
                                  Row(
                                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                    children: [
                                      Row(
                                        children: [
                                          Container(
                                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                                            decoration: BoxDecoration(
                                              color: idx == 0
                                                  ? const Color(0xFFDC2626)
                                                  : (idx < 3 ? const Color(0xFFD97706) : const Color(0xFF64748B)),
                                              borderRadius: BorderRadius.circular(6),
                                            ),
                                            child: Text(
                                              '#${item.rank}',
                                              style: const TextStyle(
                                                color: Colors.white,
                                                fontWeight: FontWeight.bold,
                                                fontSize: 11,
                                              ),
                                            ),
                                          ),
                                          const SizedBox(width: 8),
                                          Text(
                                            item.nomorTiket,
                                            style: const TextStyle(
                                              fontWeight: FontWeight.bold,
                                              fontSize: 13,
                                              color: Color(0xFF1E3A8A),
                                            ),
                                          ),
                                          const SizedBox(width: 6),
                                          Text(
                                            '· ${item.status}',
                                            style: TextStyle(fontSize: 12, color: Colors.grey.shade600),
                                          ),
                                        ],
                                      ),

                                      // Skor Urgensi Badge
                                      Container(
                                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                        decoration: BoxDecoration(
                                          color: pBgColor,
                                          borderRadius: BorderRadius.circular(16),
                                          border: Border.all(color: pColor.withValues(alpha: 0.3)),
                                        ),
                                        child: Row(
                                          children: [
                                            Icon(Icons.bolt, size: 14, color: pColor),
                                            const SizedBox(width: 2),
                                            Text(
                                              '${item.skorUrgensi} Pts',
                                              style: TextStyle(
                                                color: pColor,
                                                fontWeight: FontWeight.bold,
                                                fontSize: 12,
                                              ),
                                            ),
                                          ],
                                        ),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 10),

                                  // Judul & Lokasi
                                  Text(
                                    '${item.kategori} rusak – ${item.lokasi}',
                                    style: const TextStyle(
                                      fontWeight: FontWeight.bold,
                                      fontSize: 15,
                                      color: Color(0xFF0F172A),
                                    ),
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    'Pelapor: ${item.namaPelapor ?? "Pelapor"} · Kondisi: ${item.tingkatKeparahan}',
                                    style: TextStyle(fontSize: 12, color: Colors.grey.shade600),
                                  ),
                                  const SizedBox(height: 12),

                                  // Mini Bar Breakdown
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                                    decoration: BoxDecoration(
                                      color: const Color(0xFFF8FAFC),
                                      borderRadius: BorderRadius.circular(8),
                                    ),
                                    child: Row(
                                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                      children: [
                                        _buildMiniMetric('Keparahan (40%)', '+${item.breakdown.keparahanSubskor.toStringAsFixed(0)}'),
                                        _buildMiniMetric('Frekuensi (30%)', '+${item.breakdown.frekuensiSubskor.toStringAsFixed(0)}'),
                                        _buildMiniMetric('Dampak (30%)', '+${item.breakdown.dampakSubskor.toStringAsFixed(0)}'),
                                      ],
                                    ),
                                  ),
                                  const SizedBox(height: 14),

                                  // Tombol Aksi
                                  Row(
                                    children: [
                                      Expanded(
                                        child: OutlinedButton(
                                          onPressed: () => _showScoreDetailSheet(context, item),
                                          style: OutlinedButton.styleFrom(
                                            foregroundColor: const Color(0xFF1E3A8A),
                                            side: const BorderSide(color: Color(0xFFCBD5E1)),
                                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                                            padding: const EdgeInsets.symmetric(vertical: 10),
                                          ),
                                          child: const Text('Rincian Skor', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600)),
                                        ),
                                      ),
                                      const SizedBox(width: 8),
                                      Expanded(
                                        child: ElevatedButton(
                                          onPressed: () => _openReportDetail(context, item),
                                          style: ElevatedButton.styleFrom(
                                            backgroundColor: const Color(0xFF1E3A8A),
                                            foregroundColor: Colors.white,
                                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                                            padding: const EdgeInsets.symmetric(vertical: 10),
                                          ),
                                          child: const Text('Tindak Lanjuti', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                                        ),
                                      ),
                                    ],
                                  ),
                                ],
                              ),
                            ),
                          );
                        },
                      ),
                  ],
                ),
              ),
            ),
    );
  }

  static Widget _buildKpiCard({
    required String label,
    required String value,
    required Color color,
    required Color bgColor,
  }) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withValues(alpha: 0.2)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            value,
            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: color),
          ),
          const SizedBox(height: 2),
          Text(
            label,
            style: TextStyle(fontSize: 11, fontWeight: FontWeight.w500, color: color.withValues(alpha: 0.8)),
          ),
        ],
      ),
    );
  }

  static Widget _buildMiniMetric(String label, String value) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: const TextStyle(fontSize: 10.5, color: Color(0xFF64748B)),
        ),
        Text(
          value,
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: Color(0xFF0F172A)),
        ),
      ],
    );
  }
}
