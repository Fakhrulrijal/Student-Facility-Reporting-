import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../widgets/custom_text_field.dart';
import '../../widgets/error_dialog.dart';
import '../home/home_screen.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({Key? key}) : super(key: key);

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final TextEditingController _namaController = TextEditingController();
  final TextEditingController _nimController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  String _selectedRole = 'Mahasiswa';
  final List<String> _roleOptions = ['Mahasiswa', 'Dosen', 'Admin'];

  String? _namaError;
  String? _nimError;
  String? _emailError;
  String? _passwordError;
  bool _obscurePassword = true;

  @override
  void dispose() {
    _namaController.dispose();
    _nimController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _validateAndRegister() async {
    setState(() {
      _namaError = null;
      _nimError = null;
      _emailError = null;
      _passwordError = null;
    });

    final nama = _namaController.text.trim();
    final nim = _nimController.text.trim();
    final email = _emailController.text.trim().toLowerCase();
    final password = _passwordController.text;

    bool hasError = false;

    if (nama.isEmpty || nama.length < 2) {
      _namaError = 'Nama lengkap minimal 2 karakter';
      hasError = true;
    }

    // Validasi 8 digit angka (Sesuai Spesifikasi MOD-01 & Slide 5)
    if (!RegExp(r'^\d{8}$').hasMatch(nim)) {
      _nimError = 'NIM harus 8 digit angka';
      hasError = true;
    }

    // Validasi Domain Email @kampus.ac.id
    if (!RegExp(r'^[^@\s]+@[^@\s]+\.[^@\s]+$').hasMatch(email) || !email.endsWith('@kampus.ac.id')) {
      _emailError = 'Email wajib menggunakan domain resmi (@kampus.ac.id)';
      hasError = true;
    }

    // Validasi Password min 8 karakter
    if (password.length < 8) {
      _passwordError = 'Password minimal 8 karakter';
      hasError = true;
    }

    if (hasError) {
      setState(() {});
      ErrorDialog.show(
        context,
        title: 'Registrasi – Data Tidak Valid',
        message: 'Mohon periksa kembali kolom isian yang bertanda merah sebelum melanjutkan pendaftaran.',
        buttonText: 'Perbaiki Data',
      );
      return;
    }

    final auth = Provider.of<AuthProvider>(context, listen: false);
    final success = await auth.register(
      nama: nama,
      nomorInduk: nim,
      email: email,
      password: password,
      role: _selectedRole,
    );

    if (success && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Akun berhasil didaftarkan! Selamat datang di aplikasi.'),
          backgroundColor: Colors.green,
        ),
      );
      Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (_) => const HomeScreen()),
        (route) => false,
      );
    } else if (mounted) {
      ErrorDialog.show(
        context,
        title: 'Registrasi Gagal',
        message: auth.errorMessage ?? 'Terjadi kesalahan sistem saat mendaftarkan akun.',
      );
    }
  }

  // Simulasi Skenario Data Tidak Valid (Slide 5 Mockup)
  void _simulateInvalidData() {
    setState(() {
      _namaController.text = 'Andrean';
      _nimController.text = '1234'; // Tidak valid (< 8 digit)
      _emailController.text = 'andrean@kampus.ac.id';
      _passwordController.text = '123'; // Tidak valid (< 8 karakter)
      _selectedRole = 'Mahasiswa';
    });
    _validateAndRegister();
  }

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text(
          'Registrasi Akun',
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
        ),
        backgroundColor: Colors.white,
        foregroundColor: const Color(0xFF1E3A8A),
        elevation: 0,
        centerTitle: true,
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Input Nama Lengkap
              CustomTextField(
                controller: _namaController,
                label: 'Nama Lengkap',
                hint: 'Nama sesuai KTM',
                errorText: _namaError,
                prefixIcon: const Icon(Icons.person_outline, color: Color(0xFF1E3A8A)),
              ),
              const SizedBox(height: 16),

              // Input NIM / NIP
              CustomTextField(
                controller: _nimController,
                label: 'NIM / NIP',
                hint: 'Masukkan NIM (8 digit angka)',
                keyboardType: TextInputType.number,
                errorText: _nimError,
                prefixIcon: const Icon(Icons.badge_outlined, color: Color(0xFF1E3A8A)),
              ),
              const SizedBox(height: 16),

              // Input Email Kampus
              CustomTextField(
                controller: _emailController,
                label: 'Email Kampus',
                hint: 'nama@kampus.ac.id',
                keyboardType: TextInputType.emailAddress,
                errorText: _emailError,
                prefixIcon: const Icon(Icons.email_outlined, color: Color(0xFF1E3A8A)),
              ),
              const SizedBox(height: 16),

              // Input Password
              CustomTextField(
                controller: _passwordController,
                label: 'Password',
                hint: 'Minimal 8 karakter',
                obscureText: _obscurePassword,
                errorText: _passwordError,
                prefixIcon: const Icon(Icons.lock_outline_rounded, color: Color(0xFF1E3A8A)),
                suffixIcon: IconButton(
                  icon: Icon(
                    _obscurePassword ? Icons.visibility_off_outlined : Icons.visibility_outlined,
                    color: Colors.grey.shade600,
                  ),
                  onPressed: () {
                    setState(() {
                      _obscurePassword = !_obscurePassword;
                    });
                  },
                ),
              ),
              const SizedBox(height: 16),

              // Pilihan Peran / Role
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Peran',
                    style: TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.w600,
                      color: Color(0xFF2D3748),
                    ),
                  ),
                  const SizedBox(height: 6),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 14),
                    decoration: BoxDecoration(
                      color: const Color(0xFFF7FAFC),
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: Colors.grey.shade300),
                    ),
                    child: DropdownButtonHideUnderline(
                      child: DropdownButton<String>(
                        value: _selectedRole,
                        isExpanded: true,
                        items: _roleOptions.map((role) {
                          return DropdownMenuItem<String>(
                            value: role,
                            child: Text(
                              role,
                              style: const TextStyle(fontSize: 14, color: Color(0xFF2D3748)),
                            ),
                          );
                        }).toList(),
                        onChanged: (val) {
                          if (val != null) {
                            setState(() {
                              _selectedRole = val;
                            });
                          }
                        },
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 28),

              // Tombol Daftar
              SizedBox(
                height: 48,
                child: ElevatedButton(
                  onPressed: auth.isLoading ? null : _validateAndRegister,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF1E3A8A),
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10),
                    ),
                  ),
                  child: auth.isLoading
                      ? const SizedBox(
                          width: 22,
                          height: 22,
                          child: CircularProgressIndicator(
                            color: Colors.white,
                            strokeWidth: 2.5,
                          ),
                        )
                      : Text(
                          _nimError != null || _passwordError != null ? 'Perbaiki & Daftar' : 'Daftar',
                          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                        ),
                ),
              ),
              const SizedBox(height: 24),

              // Skenario Simulasi Slide 4 & 5
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: const Color(0xFFFEF2F2),
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: Colors.red.shade200),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      '🧪 PENGUJIAN SKENARIO DIAGRAM 1:',
                      style: TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                        color: Colors.red,
                        letterSpacing: 0.5,
                      ),
                    ),
                    const SizedBox(height: 8),
                    ActionChip(
                      avatar: const Icon(Icons.bug_report, size: 16, color: Colors.red),
                      label: const Text('Uji skenario: data tidak valid (Slide 5)'),
                      onPressed: _simulateInvalidData,
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
