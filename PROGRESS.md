# PROGRESS.md — PortalPelanggan (MyTekno)

## Current State
- Last commit: 4511acc (`feat(portalpelanggan): make MyTekno fullstack standalone with FastAPI backend, public assets, and tests`)
- Test status:
  - Frontend `npm run build`: Passing (`698ms`).
  - Smoke test FastAPI (`app.portal.main:app`): `GET /` `200`, `/tekno-indo-logo.png` `200`, `/mascots/menyapa.svg` `200`, `/portal/api/speedtest/ping` `200 pong`.
  - `pytest tests/`: **45 passed** (4 failed + 3 errors di test DB semata-mata karena MySQL lokal `127.0.0.1:33070` offline saat pengujian).
- Active module: Ekosistem 3-Repo Mandiri (`portalpelanggan`, `portalnoc`, `portalvendor`).
- Baseline: Green (Fullstack mandiri tanpa ketergantungan ke `EdTeknoGuard` maupun `portalnoc`).

## Next Steps
- [x] Jadikan `portalpelanggan` fullstack mandiri (React + FastAPI + `public/` + test suite khusus portal) (`4511acc`)
- [x] Dokumentasikan arsitektur ekosistem 3-repo (`portalvendor`, `portalnoc`, `portalpelanggan`) di file `.md`
- [x] Sinkronkan Master Contract 3-repo di [ECOSYSTEM_SYNC.md](ECOSYSTEM_SYNC.md) (`portalvendor` port `:9000/:5175`, Tahap 1 sebelum Tahap 2)
- [ ] **Tahap 2 (Refaktor Fitur Statik -> Dinamis):** Buat `app/portal/core/feature_guard.py` untuk verifikasi `Ed25519` signed policy & lindungi seluruh router di [api_router.py](app/portal/api_router.py) (`dashboard_ont`, `billing_va`, `quota_fup`, `wifi_management`, `connected_devices`, `speedtest`, `tickets`, `gps_lock`)
- [ ] **Tahap 2 (Branding Endpoint):** Tambahkan endpoint publik `GET /portal/api/config/branding` (menggabungkan `features` + `theme` dari `portalvendor` dengan `logo_url` + `brand_name` lokal)
- [ ] **Tahap 2 (Frontend Dinamis):** Refaktor tab statis `grid-cols-5` dan branding `TeknoCust` di [PortalNavigation.jsx](src/portal/components/layout/PortalNavigation.jsx) serta [PortalCustomerApp.jsx](src/portal/PortalCustomerApp.jsx) agar dinamis mengikuti policy dan logo ISP
- [ ] **Tahap 3 (E2E):** Uji end-to-end dengan MySQL lokal menyala dan `portalvendor` Control Plane (`:9000/:5175`) tanpa menyentuh server live `portal.teknoindo.net/portal/`
