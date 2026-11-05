import 'package:flutter/material.dart';
import '../models/timeline_model.dart';

class VerticalTimelineWidget extends StatelessWidget {
  final List<TimelineStageModel> stages;

  const VerticalTimelineWidget({Key? key, required this.stages}) : super(key: key);

  String _formatTimestamp(String? iso) {
    if (iso == null || iso.isEmpty || iso == '–') return '–';
    try {
      final dt = DateTime.parse(iso).toLocal();
      final months = [
        '', 'Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'
      ];
      final hour = dt.hour.toString().padLeft(2, '0');
      final min = dt.minute.toString().padLeft(2, '0');
      return '${dt.day} ${months[dt.month]} ${dt.year}, $hour:$min';
    } catch (_) {
      return iso;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: List.generate(stages.length, (index) {
        final stage = stages[index];
        final isLast = index == stages.length - 1;

        return IntrinsicHeight(
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Kolom Indikator Titik & Garis Penghubung
              Column(
                children: [
                  Container(
                    width: 28,
                    height: 28,
                    decoration: BoxDecoration(
                      color: stage.isCompleted
                          ? const Color(0xFF1E3A8A)
                          : stage.isCurrent
                              ? const Color(0xFF3B82F6)
                              : const Color(0xFFE2E8F0),
                      shape: BoxShape.circle,
                      border: Border.all(
                        color: stage.isCurrent ? const Color(0xFF93C5FD) : Colors.transparent,
                        width: 3,
                      ),
                    ),
                    child: Center(
                      child: stage.isCompleted
                          ? const Icon(Icons.check, size: 16, color: Colors.white)
                          : stage.isCurrent
                              ? Container(
                                  width: 8,
                                  height: 8,
                                  decoration: const BoxDecoration(
                                    color: Colors.white,
                                    shape: BoxShape.circle,
                                  ),
                                )
                              : Container(
                                  width: 8,
                                  height: 8,
                                  decoration: const BoxDecoration(
                                    color: Color(0xFF94A3B8),
                                    shape: BoxShape.circle,
                                  ),
                                ),
                    ),
                  ),
                  if (!isLast)
                    Expanded(
                      child: Container(
                        width: 2.5,
                        margin: const EdgeInsets.symmetric(vertical: 4),
                        color: stage.isCompleted ? const Color(0xFF1E3A8A) : const Color(0xFFE2E8F0),
                      ),
                    ),
                ],
              ),
              const SizedBox(width: 16),

              // Kolom Konten Status & Catatan
              Expanded(
                child: Padding(
                  padding: EdgeInsets.only(bottom: isLast ? 0 : 28.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            stage.stageName,
                            style: TextStyle(
                              fontSize: 15,
                              fontWeight: stage.isCurrent || stage.isCompleted
                                  ? FontWeight.bold
                                  : FontWeight.w500,
                              color: stage.isCurrent || stage.isCompleted
                                  ? const Color(0xFF1E293B)
                                  : const Color(0xFF94A3B8),
                            ),
                          ),
                          if (stage.isCurrent)
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                              decoration: BoxDecoration(
                                color: const Color(0xFFEFF6FF),
                                borderRadius: BorderRadius.circular(10),
                              ),
                              child: const Text(
                                'Saat Ini',
                                style: TextStyle(
                                  fontSize: 10,
                                  color: Color(0xFF1D4ED8),
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                        ],
                      ),
                      const SizedBox(height: 3),
                      Text(
                        _formatTimestamp(stage.timestamp),
                        style: TextStyle(
                          fontSize: 12,
                          color: stage.timestamp != null ? Colors.grey.shade600 : Colors.grey.shade400,
                        ),
                      ),
                      if (stage.catatan != null && stage.catatan!.isNotEmpty && stage.catatan != '–') ...[
                        const SizedBox(height: 8),
                        Container(
                          padding: const EdgeInsets.all(10),
                          decoration: BoxDecoration(
                            color: const Color(0xFFF8FAFC),
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: const Color(0xFFE2E8F0)),
                          ),
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Icon(Icons.notes_rounded, size: 16, color: Color(0xFF64748B)),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Text(
                                  stage.catatan!,
                                  style: const TextStyle(
                                    fontSize: 12,
                                    color: Color(0xFF334155),
                                    height: 1.3,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
              ),
            ],
          ),
        );
      }),
    );
  }
}
