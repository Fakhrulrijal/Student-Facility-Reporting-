class UserModel {
  final String idUser;
  final String nama;
  final String email;
  final String role;
  final String nomorInduk;
  final String? createdAt;

  UserModel({
    required this.idUser,
    required this.nama,
    required this.email,
    required this.role,
    required this.nomorInduk,
    this.createdAt,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      idUser: json['id_user'] ?? '',
      nama: json['nama'] ?? '',
      email: json['email'] ?? '',
      role: json['role'] ?? 'Mahasiswa',
      nomorInduk: json['nomor_induk'] ?? '',
      createdAt: json['created_at'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id_user': idUser,
      'nama': nama,
      'email': email,
      'role': role,
      'nomor_induk': nomorInduk,
      'created_at': createdAt,
    };
  }
}
