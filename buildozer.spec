[app]
title = Maps Notification Reader
package.name = mapsnotificationreader
package.domain = com.yourpackage

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 0.1
requirements = python3,kivy==2.1.0,pyjnius==1.4.2,android

# Optimized for ArtemSBulgakov/buildozer-action
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 0

[app:android]
# Permissions
android.permissions = BIND_NOTIFICATION_LISTENER_SERVICE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,WAKE_LOCK,VIBRATE

# API versions (compatible with buildozer-action)
android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 30

# Gradle settings
android.accept_sdk_license = True
android.gradle_repositories = google(), mavenCentral()
android.gradle = 7.1.1

# Java source directory
android.add_java_dir = java

# Use custom AndroidManifest template
android.manifest_template = templates/AndroidManifest.tmpl.xml

# Architecture (optimized for most devices)
android.archs = arm64-v8a, armeabi-v7a

# Service declarations
android.add_activities = com.yourpackage.notificationreader.MapsNotificationListener

# Debug settings
android.debug = 1

[buildozer:global]
log_level = 2
warn_on_root = 0