# DECISIONS.md — Architecture Decision Records (ADR)

## ADR-001: Pemisahan Fullstack Mandiri dari `EdTeknoGuard` / `portalnoc`
- **Status:** Diterima & Diimplementasikan (`4511acc`)
- **Konteks:** `portalpelanggan` ingin dijual sebagai produk terpisah dari `portalnoc`. Awalnya repo ini hanya berisi frontend React yang melakukan proxy ke port `7890`.
- **Keputusan:** Memindahkan backend FastAPI `app/portal/` beserta layanan intinya (`ont_scraper_service`, `connected_device_service`, `network_bill_service`, `fcm_service`, `mikrotik_service`, `scraper/*`), aset `public/`, dan test suite ke `portalpelanggan` agar berjalan fullstack mandiri pada port `8001`.

## ADR-002: Integrasi Control Plane `portalvendor` & Driver Modem per ISP
- **Status:** Diterima (Arsitektur Aktif)
- **Konteks:** Tiap ISP pembeli dapat memiliki kombinasi modem ONT yang berbeda, serta paket fitur berbayar dan branding yang berbeda-beda.
- **Keputusan:**
  - Komunikasi modem ONT tetap memakai adapter `app/services/scraper/driver_registry.py` di instance Data Plane masing-masing ISP.
  - Status aktif fitur (`features`) dan warna tema dikontrol oleh Vendor via signed policy (`Ed25519`) dari **`portalvendor`**, sementara **Logo & Nama Brand** mengikuti konfigurasi lokal ISP.

## ADR-003: Rencana Refaktor Fitur Statik ke Dynamic `FeatureGuard` & Sinkronisasi `ECOSYSTEM_SYNC.md`
- **Status:** Diterima (Masuk Antrean Tahap 2 setelah `portalvendor` siap)
- **Konteks:** Saat ini seluruh router di `app/portal/api_router.py` dan navigasi di `src/portal/components/layout/PortalNavigation.jsx` (`PortalBottomNav` `grid-cols-5` statis & `PortalNavbar` `TeknoCust`) serta `src/portal/PortalCustomerApp.jsx` masih bersifat statik.
- **Keputusan:**
  - Menjadikan [ECOSYSTEM_SYNC.md](ECOSYSTEM_SYNC.md) sebagai kontrak tersinkron antar 3 repo (`portalvendor` pada port `:9000/:5175`, `portalnoc` pada `:7890/:7891`, `portalpelanggan` pada `:8001/:7891`).
  - Menjadwalkan refaktor `portalpelanggan` pada Tahap 2 untuk memindahkan navigasi & endpoint dari statik menjadi dinamis via `app/portal/core/feature_guard.py` dan `GET /portal/api/config/branding`, tanpa menyentuh server live `portal.teknoindo.net/portal/`.
