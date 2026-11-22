import os
import sys
import shutil
import zipfile
import urllib.request
import subprocess

SDK_ROOT = r"D:\AndroidSdk"
JDK_DIR = os.path.join(SDK_ROOT, "jdk-17")
CMDLINE_DIR = os.path.join(SDK_ROOT, "cmdline-tools", "latest")
TEMP_DIR = os.path.join(SDK_ROOT, "downloads")

JDK_URL = "https://api.adoptium.net/v3/binary/latest/17/ga/windows/x64/jdk/hotspot/normal/eclipse?project=jdk"
CMDLINE_URL = "https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip"

def download_file(url, target_path, label):
    if os.path.exists(target_path):
        print(f"[{label}] File sudah ada: {target_path}")
        return
    print(f"[{label}] Mulai mengunduh dari: {url}")
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(target_path, "wb") as out_file:
        total_size = int(resp.headers.get("Content-Length", 0))
        downloaded = 0
        chunk_size = 1024 * 1024 # 1MB
        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            out_file.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                mb_down = downloaded / (1024 * 1024)
                mb_tot = total_size / (1024 * 1024)
                print(f"\r[{label}] Progress: {percent:.1f}% ({mb_down:.1f}/{mb_tot:.1f} MB)", end="", flush=True)
            else:
                print(f"\r[{label}] Downloaded: {downloaded / (1024*1024):.1f} MB", end="", flush=True)
    print(f"\n[{label}] Selesai mengunduh.")

def extract_zip(zip_path, extract_dir, label):
    print(f"[{label}] Mengekstrak ke: {extract_dir}")
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_dir)
    print(f"[{label}] Ekstraksi selesai.")

def setup_jdk():
    # Periksa apakah java.exe sudah ada
    java_exe = os.path.join(JDK_DIR, "bin", "java.exe")
    if os.path.exists(java_exe):
        print(f"[JDK] JDK 17 sudah siap di {JDK_DIR}")
        return JDK_DIR
    
    jdk_zip = os.path.join(TEMP_DIR, "jdk17.zip")
    download_file(JDK_URL, jdk_zip, "JDK-17")
    
    # Ekstrak sementara lalu pindahkan isinya
    temp_extract = os.path.join(TEMP_DIR, "jdk_extracted")
    extract_zip(jdk_zip, temp_extract, "JDK-17")
    
    # Cari subfolder jdk-17.*
    subfolders = [f for f in os.listdir(temp_extract) if os.path.isdir(os.path.join(temp_extract, f))]
    source_dir = os.path.join(temp_extract, subfolders[0]) if subfolders else temp_extract
    
    if os.path.exists(JDK_DIR):
        shutil.rmtree(JDK_DIR)
    shutil.move(source_dir, JDK_DIR)
    shutil.rmtree(temp_extract, ignore_errors=True)
    print(f"[JDK] Sukses menyiapkan JDK 17 di {JDK_DIR}")
    return JDK_DIR

def setup_cmdline_tools():
    sdkmanager_bat = os.path.join(CMDLINE_DIR, "bin", "sdkmanager.bat")
    if os.path.exists(sdkmanager_bat):
        print(f"[Android Tools] cmdline-tools sudah siap di {CMDLINE_DIR}")
        return CMDLINE_DIR

    cmdline_zip = os.path.join(TEMP_DIR, "cmdline-tools.zip")
    download_file(CMDLINE_URL, cmdline_zip, "Cmdline-Tools")
    
    temp_extract = os.path.join(TEMP_DIR, "cmdline_extracted")
    extract_zip(cmdline_zip, temp_extract, "Cmdline-Tools")
    
    # Isi cmdline-tools berada dalam folder cmdline-tools/
    source_dir = os.path.join(temp_extract, "cmdline-tools")
    os.makedirs(os.path.dirname(CMDLINE_DIR), exist_ok=True)
    if os.path.exists(CMDLINE_DIR):
        shutil.rmtree(CMDLINE_DIR)
    shutil.move(source_dir, CMDLINE_DIR)
    shutil.rmtree(temp_extract, ignore_errors=True)
    print(f"[Android Tools] Sukses menyiapkan cmdline-tools di {CMDLINE_DIR}")
    return CMDLINE_DIR

def get_env():
    env = os.environ.copy()
    env["JAVA_HOME"] = JDK_DIR
    env["ANDROID_HOME"] = SDK_ROOT
    env["ANDROID_SDK_ROOT"] = SDK_ROOT
    jdk_bin = os.path.join(JDK_DIR, "bin")
    cmdline_bin = os.path.join(CMDLINE_DIR, "bin")
    platform_tools_bin = os.path.join(SDK_ROOT, "platform-tools")
    env["PATH"] = f"{jdk_bin};{cmdline_bin};{platform_tools_bin};C:\\src\\flutter\\bin;" + env.get("PATH", "")
    return env

def install_android_packages():
    print("\n[Android SDK] Menginstal platform-tools, platforms;android-34, dan build-tools;34.0.0...")
    sdkmanager = os.path.join(CMDLINE_DIR, "bin", "sdkmanager.bat")
    env = get_env()
    
    # 1. Accept licenses otomatis
    print("[Android SDK] Menyetujui lisensi SDK...")
    p = subprocess.Popen(
        f'"{sdkmanager}" --licenses --sdk_root="{SDK_ROOT}"',
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        text=True
    )
    # Kirim 'y' berulang kali untuk accept semua lisensi
    yes_input = "y\n" * 50
    out, _ = p.communicate(input=yes_input)
    print(f"[Android SDK] License status: {p.returncode}")

    # 2. Install platform-tools, android-34, build-tools 34.0.0
    packages = ["platform-tools", "platforms;android-34", "build-tools;34.0.0"]
    for pkg in packages:
        print(f"[Android SDK] Menginstal paket: {pkg}...")
        cmd = f'"{sdkmanager}" "{pkg}" --sdk_root="{SDK_ROOT}"'
        p2 = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
        if p2.returncode == 0:
            print(f"[Android SDK] {pkg} berhasil terpasang.")
        else:
            print(f"[Android SDK] Error pasang {pkg}: {p2.stdout}\n{p2.stderr}")

def configure_flutter():
    print("\n[Flutter] Menghubungkan Flutter dengan Android SDK & JDK...")
    env = get_env()
    subprocess.run(f'flutter config --android-sdk "{SDK_ROOT}"', shell=True, env=env)
    subprocess.run(f'flutter config --jdk-dir "{JDK_DIR}"', shell=True, env=env)
    subprocess.run('flutter doctor', shell=True, env=env)

def build_apk():
    print("\n=======================================================")
    print("[Flutter] MEMULAI PROSES BUILD ANDROID APK (DEBUG)...")
    print("=======================================================")
    env = get_env()
    cmd = "flutter build apk --debug"
    res = subprocess.run(cmd, shell=True, env=env)
    
    apk_source = r"build\app\outputs\flutter-apk\app-debug.apk"
    if os.path.exists(apk_source):
        print(f"\n[SUKSES] File APK berhasil dibuat di: {apk_source}")
        
        # Salin ke root folder agar mudah diakses
        target_root = r"Aplikasi_Fasilitas_Kampus.apk"
        shutil.copy2(apk_source, target_root)
        print(f"[SUKSES] Salinan file APK siap di: {os.path.abspath(target_root)}")
        
        # Salin juga ke build/web agar bisa didownload langsung via link browser di HP
        target_web = r"build\web\app-debug.apk"
        if os.path.exists(r"build\web"):
            shutil.copy2(apk_source, target_web)
            print(f"[SUKSES] Salinan web download siap di: {os.path.abspath(target_web)}")
    else:
        print("\n[PERINGATAN] File APK tidak ditemukan di path output.")

if __name__ == "__main__":
    os.makedirs(TEMP_DIR, exist_ok=True)
    setup_jdk()
    setup_cmdline_tools()
    install_android_packages()
    configure_flutter()
    build_apk()
