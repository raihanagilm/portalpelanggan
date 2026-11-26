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
  - Status aktif fitur (`features`) dan warna tema dikontrol oleh Vendor via signed policy dari **`portalvendor`**, sementara **Logo & Nama Brand** mengikuti konfigurasi lokal ISP.
