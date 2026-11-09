import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/auth_provider.dart';
import 'providers/report_provider.dart';
import 'providers/admin_provider.dart';
import 'providers/analytics_provider.dart';
import 'providers/priority_provider.dart';
import 'screens/auth/login_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const StudentFacilityReportingApp());
}

class StudentFacilityReportingApp extends StatelessWidget {
  const StudentFacilityReportingApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => ReportProvider()),
        ChangeNotifierProvider(create: (_) => AdminProvider()),
        ChangeNotifierProvider(create: (_) => AnalyticsProvider()),
        ChangeNotifierProvider(create: (_) => PriorityProvider()),
      ],
      child: MaterialApp(
        title: 'Student Facility Reporting',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          useMaterial3: true,
          colorScheme: ColorScheme.fromSeed(
            seedColor: const Color(0xFF1E3A8A),
            primary: const Color(0xFF1E3A8A),
            secondary: const Color(0xFF2563EB),
          ),
          scaffoldBackgroundColor: Colors.white,
          fontFamily: 'Roboto',
          appBarTheme: const AppBarTheme(
            backgroundColor: Colors.white,
            foregroundColor: Color(0xFF1E3A8A),
            elevation: 0,
            centerTitle: true,
          ),
        ),
        home: const LoginScreen(),
      ),
    );
  }
}
