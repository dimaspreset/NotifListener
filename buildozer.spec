[app]
# Nama aplikasi
title = CuyBotApp
package.name = cuybot
package.domain = com

# Versi aplikasi
version = 0.1

# File utama Python kamu
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Entry point
main.py = main.py

# Icon (opsional)
#icon.filename = %(source.dir)s/data/icon.png

# Requirements
requirements = python3,kivy,kivymd,pyjnius,android
android.api = 33
android.minapi = 24
android.ndk = 25b
android.enable_androidx = True

# Firebase (opsional, kalau mau tetap nyimpen ke Firebase)
android.gradle_dependencies = com.google.firebase:firebase-database:20.3.0

# Tambahkan Java dan manifest custom
android.add_src = ./android
android.manifest_xml = ./android/AndroidManifest.xml

# Orientasi layar
orientation = portrait

# Presplash screen (opsional)
#presplash.filename = %(source.dir)s/data/presplash.png

# Jangan optimasi Python agar tetap kompatibel
# (supaya Pyjnius dan service Java aman)
android.compile_options = "sourceCompatibility=1.8,targetCompatibility=1.8"

# Permissions (opsional tambahan selain manifest)
android.permissions = INTERNET,RECEIVE_BOOT_COMPLETED,WAKE_LOCK,FOREGROUND_SERVICE

# Support multiple architectures (opsional)
android.archs = armeabi-v7a, arm64-v8a

# Package ke format APK
package.format = apk

# Jalankan Python di main thread
android.main = main

[buildozer]
log_level = 2
warn_on_root = 1

[log]
log_level = 2
