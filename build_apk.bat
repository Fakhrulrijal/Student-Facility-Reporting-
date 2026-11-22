@echo off
set "JAVA_HOME=D:\AndroidSdk\jdk-17"
set "ANDROID_HOME=D:\AndroidSdk"
set "ANDROID_SDK_ROOT=D:\AndroidSdk"
set "PATH=D:\AndroidSdk\jdk-17\bin;D:\AndroidSdk\cmdline-tools\latest\bin;D:\AndroidSdk\platform-tools;C:\src\flutter\bin;%PATH%"

echo Building Native Android APK (ARM64)...
call flutter build apk --debug --target-platform android-arm64

if exist "build\app\outputs\flutter-apk\app-debug.apk" (
    copy /y "build\app\outputs\flutter-apk\app-debug.apk" "Aplikasi_Fasilitas_Kampus.apk"
    if exist "build\web" (
        copy /y "build\app\outputs\flutter-apk\app-debug.apk" "build\web\app-debug.apk"
    )
    echo SUCCESS_APK_CREATED
) else (
    echo FAILED_APK_NOT_FOUND
)
