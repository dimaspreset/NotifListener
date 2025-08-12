# Maps Notification Reader

![Build Status](https://github.com/yourusername/maps-notification-reader/workflows/Build%20Android%20APK/badge.svg)

Aplikasi Android yang menggunakan Notification Listener untuk mengambil data navigasi dari Google Maps secara real-time.

## 🚀 Features

- ✅ Real-time detection notifikasi Google Maps
- ✅ Ekstrak data navigasi (arah, jarak, waktu)
- ✅ Simpan data dalam format JSON
- ✅ Interface Kivy yang simpel dan fungsional
- ✅ Auto-build dengan GitHub Actions
- ✅ Support Android 5.0+ (API 21)

## 📱 Screenshots

*Coming soon...*

## 🔧 Quick Start

### Option 1: Download Pre-built APK
1. Go to [Releases](https://github.com/yourusername/maps-notification-reader/releases)
2. Download latest APK
3. Install di Android device
4. Enable Notification Access permission

### Option 2: Build dengan GitHub Actions
1. Fork repository ini
2. Push ke branch `main` atau buat tag `v1.0.0`
3. GitHub Actions akan otomatis build APK
4. Download dari Actions artifacts

### Option 3: Build Local
```bash
git clone https://github.com/yourusername/maps-notification-reader.git
cd maps-notification-reader
buildozer android debug
```

## 📋 Setup Instructions

### Prerequisites
- Android device dengan Notification Access permission
- Google Maps terinstall
- Android 5.0+ (API 21)

### Installation Steps
1. Install APK ke Android device
2. Buka **Settings → Apps → Special App Access → Notification Access**
3. Enable permission untuk "Maps Notification Reader"
4. Buka Google Maps, mulai navigasi
5. Buka aplikasi, tekan "Start Listening"

## 🏗️ Development

### Project Structure
```
├── main.py                                    # Kivy main application
├── java/
│   └── MapsNotificationListener.java        # Java notification service
├── templates/
│   └── AndroidManifest.tmpl.xml            # Android manifest template
├── buildozer.spec                            # Build configuration
├── requirements.txt                          # Python dependencies (optional)
├── .github/
│   └── workflows/
│       └── build-simple.yml                # GitHub Actions workflow
└── README.md
```

### Build Locally

#### Windows (WSL Recommended)
```bash
# Install WSL
wsl --install

# In WSL terminal:
sudo apt update
sudo apt install python3-pip openjdk-8-jdk
pip3 install buildozer kivy
buildozer android debug
```

#### Linux/macOS
```bash
sudo apt install python3-pip openjdk-8-jdk
pip3 install buildozer kivy
buildozer android debug
```

### GitHub Actions Build
Every push to `main` branch atau tag `v*` akan trigger auto-build:

1. **Debug Build**: Tersedia di Actions artifacts
2. **Release Build**: Otomatis upload ke GitHub Releases (untuk tags)

## 📄 Permissions

Aplikasi memerlukan permissions berikut:
- `BIND_NOTIFICATION_LISTENER_SERVICE` - Untuk access notifikasi
- `WRITE_EXTERNAL_STORAGE` - Untuk simpan data
- `READ_EXTERNAL_STORAGE` - Untuk baca data
- `INTERNET` - Untuk future features

## 🔍 How It Works

1. **Notification Listener Service** (Java) mendeteksi notifikasi dari Google Maps
2. Data navigasi diekstrak dari notification content
3. Data disimpan dalam file JSON di app directory
4. **Kivy frontend** membaca dan menampilkan data secara real-time

## 📊 Data Format

Data tersimpan dalam format JSON:
```json
[
  {
    "timestamp": "2024-01-15 10:30:00",
    "package": "com.google.android.apps.maps",
    "title": "Google Maps Navigation",
    "text": "In 500m, turn right onto Jl. Sudirman",
    "subtext": "12 min (3.2 km) remaining"
  }
]
```

## 🐛 Troubleshooting

### APK tidak bisa install
- Enable "Install from Unknown Sources"
- Check Android version (minimum 5.0)

### Notification tidak terdeteksi
- Pastikan Notification Access permission sudah enabled
- Restart aplikasi setelah enable permission
- Test dengan memulai navigasi di Google Maps

### Build gagal di GitHub Actions
- Check Actions logs untuk error detail
- Pastikan semua file ada di repository
- Verify buildozer.spec configuration

## 🚧 Roadmap

- [ ] Filter notifikasi berdasarkan jenis
- [ ] Export data ke CSV/Excel
- [ ] Real-time map visualization
- [ ] Voice command integration
- [ ] Cloud sync backup
- [ ] Material Design UI

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

- **Your Name** - [GitHub Profile](https://github.com/yourusername)

## 🙏 Acknowledgments

- [Kivy](https://kivy.org/) - Cross-platform Python framework
- [Buildozer](https://github.com/kivy/buildozer) - Android packaging tool
- [GitHub Actions](https://github.com/features/actions) - CI/CD pipeline

---

⭐ **Star this repo if it helps you!**