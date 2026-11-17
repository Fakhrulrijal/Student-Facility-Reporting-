import 'package:flutter_test/flutter_test.dart';
import 'package:student_facility_reporting/main.dart';

void main() {
  testWidgets('App initialization test', (WidgetTester tester) async {
    await tester.pumpWidget(const StudentFacilityReportingApp());
    expect(find.byType(StudentFacilityReportingApp), findsOneWidget);
  });
}
