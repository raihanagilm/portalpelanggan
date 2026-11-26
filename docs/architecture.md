# Arsitektur Fullstack Mandiri & Integrasi Ecosystem: PortalPelanggan (MyTekno)

Dokumen ini menjelaskan struktur fullstack mandiri **PortalPelanggan (MyTekno)** dan cara terhubungnya dengan **PortalVendor (Control Plane)** serta jaringan lokal ISP.

---

## 1. Diagram Arsitektur & Ekosistem 3-Repo

```text
           +---------------------------------------------+
           |         PORTALVENDOR (Control Plane)        |
           |  Signed Policy: Status Tenant, Feature Flag |
           |  (ON/OFF), & Theme Colors                   |
           +----------------------+----------------------+
                                  |
                                  v (Policy Sync + Verify Signature)
+-------------------------------------------------------------------+
|               PORTALPELANGGAN (Fullstack Mandiri)                 |
|                                                                   |
|  Frontend (React + Vite -> dist/)                                 |
|  - Dynamic Feature Menu & White-Label Logo/Theme                  |
|  - PortalAuth, Dashboard, Payment VA, Quota, WiFi, Speedtest      |
|                               |                                   |
|                               v (/portal/api/*)                   |
|  Backend (FastAPI - app/portal/main.py, Port 8001)                |
|  - FeatureGuard Dependency (403 jika fitur dimatikan Vendor)      |
|  - Auth, Dashboard, Payment (Network Bill), Tickets, WiFi, Quota  |
|  - ONT Driver Registry (ZTE, Huawei, FiberHome, ZL2113X, XPON)    |
+---------------+---------------------------------+-----------------+
                |                                 |
                v                                 v
      MySQL Tenant Database            Jaringan Lokal ISP / Network Bill
   (pelanggan, tiket, kuota, log)       (ONT Scraper, MikroTik, VA API)
```

---

## 2. Struktur Direktori Utama

```text
portalpelanggan/
├── app/
│   ├── main.py                         # Entry point FastAPI (re-export app.portal.main)
│   ├── core/                           # Config, database/tenant session, security, lockout
│   ├── db/models.py                    # Model SQLAlchemy (MasterBase & TenantBase)
│   ├── middleware/security_middleware.py # Security Headers & Rate Limiter
│   ├── portal/
│   │   ├── main.py                     # App FastAPI, static/dist SPA, /portal/api mount
│   │   ├── api_router.py               # Aggregator router domain portal
│   │   ├── core/security.py            # Token sesi pelanggan & validasi WiFi rumah
│   │   ├── modules/                    # auth, dashboard, payment, profile, quota, speedtest, tickets, wifi
│   │   └── services/                   # customer_service, customer_activity_service
│   └── services/                       # ont_scraper_service, scraper/drivers, network_bill_service, fcm_service
├── public/                             # Logo, favicon, maskot SVG (/mascots/*.svg)
├── src/
│   ├── main.jsx                        # Root React entry (render PortalCustomerApp)
│   ├── portal/                         # Komponen UI & portalApi.js
│   └── styles/mascots/                 # Animasi CSS maskot
├── tests/                              # Unit & integration tests khusus portal
├── vite.config.js                      # Dev port 7891, proxy /portal/api -> 127.0.0.1:8001
└── package.json & requirements.txt
```

---

## 3. Aturan Kustomisasi & Perbedaan Modem Antar-ISP
- **Adapter Modem ONT:** Saat menjual ke ISP dengan merek modem baru, cukup tambahkan driver pada `app/services/scraper/drivers/` dan daftarkan di `driver_registry.py` tanpa mengubah logika portal.
- **Kontrol Fitur ON/OFF:** Ditetapkan eksklusif oleh **Vendor** melalui `portalvendor` (signed policy), dicek pada router API backend (mengembalikan `403` jika nonaktif) serta pada menu tab UI frontend.
- **Logo & Branding:** **Logo** & **Nama Brand** diambil dari aset/pengaturan lokal milik Admin ISP, sedangkan warna tema dapat mengikuti policy dari `portalvendor`.
