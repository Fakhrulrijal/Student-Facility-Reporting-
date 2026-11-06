from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.config import UPLOAD_DIR
from app.routers import auth, facilities, reports, admin

app = FastAPI(
    title="Aplikasi Pelaporan Fasilitas Kampus - REST API",
    version="1.0.0",
    description="Backend REST API untuk Student Facility Reporting (MOD-01 Autentikasi & MOD-02 Pelaporan Kerusakan & QR Scanner)"
)

# Konfigurasi CORS agar dapat diakses Flutter (Web, Mobile Emulator, Desktop)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Validation Error Handler (HTTP 422/400) agar pesan validasi rapi dan terstruktur
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = " -> ".join(str(loc) for loc in err.get("loc", []) if loc != "body")
        msg = err.get("msg")
        errors.append(f"{field}: {msg}" if field else msg)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "message": "Validasi input gagal.",
            "errors": errors
        }
    )

# Static files untuk foto yang diunggah
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# Include Routers
app.include_router(auth.router)
app.include_router(facilities.router)
app.include_router(reports.router)
app.include_router(admin.router)

@app.get("/", tags=["Health Check"])
def root():
    return {
        "status": "online",
        "app": "Aplikasi Pelaporan Fasilitas Kampus",
        "modules_active": [
            "MOD-01 Autentikasi & User Management",
            "MOD-02 Pelaporan Kerusakan & QR Scanner",
            "MOD-03 Tracking Status & Histori Laporan",
            "MOD-04 Dashboard Admin & Kelola Tiket"
        ],
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
