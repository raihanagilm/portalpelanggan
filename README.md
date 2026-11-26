# PortalPelanggan (MyTekno) 📱

**PortalPelanggan (MyTekno)** adalah aplikasi portal layanan mandiri pelanggan ISP (Web Mobile-First & Android WebView) yang beroperasi **secara fullstack mandiri** (React + Vite frontend dan Python FastAPI backend) tanpa ketergantungan kode ke `EdTeknoGuard` maupun `portalnoc`.

> **Ekosistem 3-Repo SaaS Komersial:**
> - **`portalpelanggan`** (repo ini): Customer Portal Data Plane (MyTekno).
> - **`portalnoc`** ([GitHub](https://github.com/raihanagilm/portalnoc)): Admin NOC & Telemetry Data Plane (TeknoGuard).
> - **`portalvendor`** ([GitHub](https://github.com/raihanagilm/portalvendor)): Vendor Control Plane untuk manajemen multi-tenant ISP, feature flags ON/OFF bertanda tangan, status langganan, dan tema warna.

---

## Fitur Utama Pelanggan (Dapat Dikontrol Feature Flag via `portalvendor`)
1. **Dashboard Status ONT & Redaman Optik:** Memantau status koneksi (`ONLINE`/`OFFLINE`), daya optik (`dBm`), dan pengingat status layanan.
2. **Tagihan & Virtual Account (`Network Bill API v1`):** Menampilkan tagihan aktif, kanal VA bank, riwayat pembayaran, dan pemeriksaan pelunasan real-time.
3. **Pemantauan Kuota FUP:** Melihat pemakaian kuota bulanan dan riwayat harian.
4. **Kelola WiFi & Perangkat Terhubung:** Mengganti SSID/sandi WiFi serta memblokir/membuka blokir MAC address perangkat (terproteksi validasi WiFi rumah).
5. **Speed Test Terintegrasi:** Menguji latensi (`ping`), unduh, dan unggah langsung ke server ISP.
6. **Tiket Kendala & Notifikasi Push (FCM):** Pelaporan gangguan mandiri dan sinkronisasi lokasi GPS senyap.

---

## Panduan Menjalankan Aplikasi Secara Mandiri

### 1. Prasyarat & Instalasi
Pastikan Python 3.10+ dan Node.js 18+ terpasang:
```bash
python -m pip install -r requirements.txt
npm install
```

### 2. Konfigurasi Lingkungan (`.env`)
Salin `.env.example` menjadi `.env`, lalu sesuaikan kredensial MySQL lokal/tenant ISP dan token Network Bill:
```ini
APP_NAME=MyTekno
APP_ENV=development
APP_PORT=8001
APP_URL=http://localhost:8001
```

### 3. Build Frontend & Jalankan Backend
```bash
# Build React SPA ke dist/
npm run build

# Jalankan FastAPI Backend mandiri (port 8001)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```
Untuk mode pengembangan frontend dengan Vite HMR (`http://localhost:7891`, proxy `/portal/api` → `http://127.0.0.1:8001`):
```bash
npm run dev
```

---

## Navigasi Dokumentasi
- [Kontrak & Sinkronisasi 3-Repo (ECOSYSTEM_SYNC.md)](ECOSYSTEM_SYNC.md)
- [Pedoman AI Agent (AGENTS.md)](AGENTS.md)
- [Identitas & Ruang Lingkup Produk (PRODUCT.md)](PRODUCT.md)
- [Keputusan Arsitektur (DECISIONS.md)](DECISIONS.md)
- [Arsitektur Fullstack Mandiri & Sync PortalVendor (docs/architecture.md)](docs/architecture.md)
- [Status & Rencana Pengembangan (PROGRESS.md)](PROGRESS.md)
- [Panduan Wrapper Android Studio (docs/PROMPT_ANDROID_STUDIO.md)](docs/PROMPT_ANDROID_STUDIO.md)
