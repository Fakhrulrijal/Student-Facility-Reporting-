import re
from enum import Enum
from typing import Optional
from pydantic import BaseModel, field_validator

class UserRole(str, Enum):
    MAHASISWA = "Mahasiswa"
    DOSEN = "Dosen"
    ADMIN = "Admin"

class UserRegisterRequest(BaseModel):
    nama: str
    nomor_induk: str
    email: str
    password: str
    role: UserRole = UserRole.MAHASISWA
    fakultas: Optional[str] = "Fakultas Teknik & Ilmu Komputer"
    prodi: Optional[str] = "Teknik Informatika"

    @field_validator("nama")
    @classmethod
    def validate_nama(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Nama lengkap minimal 2 karakter.")
        return v

    @field_validator("nomor_induk")
    @classmethod
    def validate_nomor_induk(cls, v: str) -> str:
        v = v.strip()
        if not re.match(r"^\d{8}$", v):
            raise ValueError("NIM / NIP harus berupa 8 digit angka.")
        return v

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, v: str) -> str:
        v_str = str(v).strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v_str):
            raise ValueError("Format email tidak valid.")
        if not v_str.endswith("@kampus.ac.id"):
            raise ValueError("Email harus menggunakan domain resmi institusi (@kampus.ac.id).")
        return v_str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password minimal terdiri dari 8 karakter.")
        return v

class UserLoginRequest(BaseModel):
    nomor_induk_atau_email: str
    password: str

class UserResponse(BaseModel):
    id_user: str
    nama: str
    email: str
    role: str
    nomor_induk: str
    created_at: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
