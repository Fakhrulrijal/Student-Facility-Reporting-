from datetime import datetime, timezone
import uuid
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.auth import UserRegisterRequest, UserLoginRequest, TokenResponse, UserResponse
from app.database.json_db import db
from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["Autentikasi & Akun"])
security = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autentikasi diperlukan. Header Authorization Bearer tidak ditemukan."
        )
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau telah kadaluarsa."
        )
    user_id = payload.get("sub")
    user = db.find_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User pemilik token tidak ditemukan di database."
        )
    return user

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegisterRequest):
    # Cek duplikasi email
    if db.find_user_by_email(str(payload.email)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{payload.email}' sudah terdaftar dalam sistem."
        )

    # Cek duplikasi NIM/NIP
    if db.find_user_by_nomor_induk(payload.nomor_induk):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"NIM / NIP '{payload.nomor_induk}' sudah terdaftar dalam sistem."
        )

    new_id_user = f"USR-{uuid.uuid4().hex[:8].upper()}"
    new_id_detail = f"DET-{uuid.uuid4().hex[:8].upper()}"
    hashed_pwd = get_password_hash(payload.password)
    now_iso = datetime.now(timezone.utc).isoformat()

    user_data = {
        "id_user": new_id_user,
        "nama": payload.nama,
        "email": str(payload.email).lower(),
        "password": hashed_pwd,
        "role": payload.role.value,
        "nomor_induk": payload.nomor_induk,
        "created_at": now_iso
    }

    detail_data = {
        "id_detail": new_id_detail,
        "id_user": new_id_user,
        "fakultas": payload.fakultas or "-",
        "prodi": payload.prodi or "-",
        "telepon": "-",
        "foto_profil": "",
        "status_aktif": True,
        "created_at": now_iso
    }

    db.add_user(user_data, detail_data)

    # Generate JWT Token
    token = create_access_token({
        "sub": new_id_user,
        "role": payload.role.value,
        "nomor_induk": payload.nomor_induk,
        "nama": payload.nama
    })

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id_user=new_id_user,
            nama=payload.nama,
            email=user_data["email"],
            role=payload.role.value,
            nomor_induk=payload.nomor_induk,
            created_at=now_iso
        )
    )

@router.post("/login", response_model=TokenResponse)
def login_user(payload: UserLoginRequest):
    identifier = payload.nomor_induk_atau_email.strip()
    user = None

    if "@" in identifier:
        user = db.find_user_by_email(identifier)
    else:
        user = db.find_user_by_nomor_induk(identifier)

    if not user or not verify_password(payload.password, user.get("password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="NIM / Email atau password salah. Silakan periksa kembali kredensial Anda."
        )

    token = create_access_token({
        "sub": user["id_user"],
        "role": user["role"],
        "nomor_induk": user["nomor_induk"],
        "nama": user["nama"]
    })

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id_user=user["id_user"],
            nama=user["nama"],
            email=user["email"],
            role=user["role"],
            nomor_induk=user["nomor_induk"],
            created_at=user.get("created_at", datetime.now(timezone.utc).isoformat())
        )
    )

@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id_user=current_user["id_user"],
        nama=current_user["nama"],
        email=current_user["email"],
        role=current_user["role"],
        nomor_induk=current_user["nomor_induk"],
        created_at=current_user.get("created_at", "")
    )
