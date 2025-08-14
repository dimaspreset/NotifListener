[app]
# Nama aplikasi
title = CuyBotApp
package.name = cuybot
package.domain = com.cuybot

# Versi aplikasi
version = 0.1

# File utama Python kamu
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# Entry point
main.py = main.py

# Icon (opsional)
#icon.filename = %(source.dir)s/data/icon.png

# Requirements - Simplified for compatibility
requirements = python3,kivy,kivymd,pyjnius,android

# Android settings - More compatible versions
android.api = 31
android.minapi = 21
android.ndk = 25b
android.enable_androidx = True
android.accept_sdk_license = True

# Firebase dependencies - Removed for now to avoid build issues
# android.gradle_dependencies = com.google.firebase:firebase-database:20.2.2, com.google.firebase:firebase-core:21.1.1
# android.gradle_plugins = com.google.gms.google-services

# Custom Java code and manifest
android.add_src = ./android

# Permissions - Complete list
android.permissions = INTERNET,BIND_NOTIFICATION_LISTENER_SERVICE,RECEIVE_BOOT_COMPLETED,WAKE_LOCK,FOREGROUND_SERVICE,ACCESS_NETWORK_STATE

# Orientasi layar
orientation = portrait

# Architecture support
android.archs = armeabi-v7a, arm64-v8a

# Package format
android.release_artifact = apk

# Additional build options
android.compile_options = "sourceCompatibility=1.8,targetCompatibility=1.8"

# Skip update check for faster builds
android.skip_update = False

[buildozer]
log_level = 2
warn_on_root = 1

[log]
log_level = 2