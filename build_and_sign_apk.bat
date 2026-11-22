@echo off
set "JAVA_HOME=D:\AndroidSdk\jdk-17"
set "ANDROID_HOME=D:\AndroidSdk"
set "PATH=D:\AndroidSdk\jdk-17\bin;D:\AndroidSdk\build-tools\36.0.0;C:\src\flutter\bin;%PATH%"

if exist "build\app\outputs\flutter-apk\app-release.apk" del /f /q "build\app\outputs\flutter-apk\app-release.apk"

echo Building APK with Target SDK 34...
call flutter build apk --release

if errorlevel 1 (
    echo BUILD_FAILED_WITH_ERROR
    exit /b 1
)

echo Signing APK with Dual V1 + V2 Signature Schemes...
set "KEYSTORE=C:\Users\LENOVO\.android\debug.keystore"
call D:\AndroidSdk\build-tools\36.0.0\apksigner.bat sign --ks "%KEYSTORE%" --ks-pass pass:android --key-pass pass:android --ks-key-alias androiddebugkey --v1-signing-enabled true --v2-signing-enabled true "build\app\outputs\flutter-apk\app-release.apk"

echo Verifying signatures...
call D:\AndroidSdk\build-tools\36.0.0\apksigner.bat verify --verbose "build\app\outputs\flutter-apk\app-release.apk"

copy /y "build\app\outputs\flutter-apk\app-release.apk" "Aplikasi_Fasilitas_Kampus.apk"
copy /y "build\app\outputs\flutter-apk\app-release.apk" "build\web\app-release.apk"
copy /y "build\app\outputs\flutter-apk\app-release.apk" "build\web\app-debug.apk"
echo SUCCESS_FINISHED
