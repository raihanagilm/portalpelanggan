# PRODUCT.md — PortalPelanggan (MyTekno)

## 1. Product Identity & Mission
- **Product Name:** MyTekno (`portalpelanggan`) — Portal Layanan Mandiri Pelanggan ISP.
- **Ecosystem Role:** Standalone Fullstack Customer Portal Data Plane in the 3-repo ISP SaaS ecosystem (`portalnoc`, `portalpelanggan`, `portalvendor`).
- **Core Mission:** Provide ISP subscribers with a mobile-first white-label portal (Web + Android WebView) to check internet & optical health, pay bills via Virtual Account, monitor quota, manage home Wi-Fi, run speed tests, and submit support tickets—sellable independently from `portalnoc` and controlled by `portalvendor`.

## 2. Target Users & Surface Mode
- **ISP Subscribers (End-Users):** Accessing via mobile browser or Android APK (`docs/PROMPT_ANDROID_STUDIO.md`).
- **Surface Mode:** `Operate` / `Persuade` — Mobile-first, high affordance, friendly mascot guidance, zero technical jargon.

## 3. Feature-Flaggable Modules (Controlled by `portalvendor`)
1. `dashboard_ont`: Status koneksi, redaman optik, dan pengingat tagihan.
2. `billing_va`: Tagihan aktif, panduan pembayaran Virtual Account, dan riwayat pembayaran.
3. `quota_fup`: Pemakaian kuota bulanan dan log harian.
4. `wifi_management`: Ubah SSID & kata sandi WiFi rumah.
5. `connected_devices`: Daftar perangkat terhubung & blokir/unblokir MAC.
6. `speedtest`: Pengujian kecepatan ping, download, dan upload.
7. `tickets`: Pelaporan kendala mandiri pelanggan.
8. `gps_lock`: Pemetaan koordinat rumah otomatis saat terhubung WiFi rumah.
