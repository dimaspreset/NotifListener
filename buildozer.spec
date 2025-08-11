[app]
title = Maps Notification Reader
package.name = mapsnotificationreader
package.domain = com.yourpackage

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 0.1
requirements = python3,kivy==2.1.0,pyjnius==1.4.2,android

# GitHub Actions optimizations
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2

# GitHub Actions optimizations
warn_on_root = 0

[app:android]
# Android specific
android.permissions = BIND_NOTIFICATION_LISTENER_SERVICE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET
android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 23b

# Optimize for CI/CD
android.accept_sdk_license = True
android.gradle_dependencies = 
android.gradle = 7.3.0

# Add Java source
android.add_java_dir = java

# Service declaration
android.add_src = java
android.add_activities = com.yourpackage.notificationreader.MapsNotificationListener

# Performance optimizations for GitHub Actions
android.gradle_repositories = google(), mavenCentral()
android.enable_androidx = True

[buildozer:global]
log_level = 2
warn_on_root = 1