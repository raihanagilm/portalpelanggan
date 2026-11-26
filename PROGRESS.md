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
- [ ] Tambahkan endpoint publik konfigurasi branding & fitur (`GET /portal/api/config/branding`)
- [ ] Implementasikan `FeatureGuard` backend + dynamic tab/theme loader di `PortalCustomerApp.jsx` yang tersinkron dengan `portalvendor`
- [ ] Uji end-to-end dengan MySQL lokal menyala dan `portalvendor` Control Plane
