# AGENTS.md — PortalPelanggan (MyTekno)

## 1. System Overview & 3-Repo Ecosystem
**PortalPelanggan (MyTekno)** is a standalone fullstack customer self-service portal (React + Vite frontend and FastAPI backend under `app/portal/`). It must remain decoupled from Admin NOC modules (`portalnoc`).

Ecosystem roles:
- **`portalpelanggan`** (`https://github.com/raihanagilm/portalpelanggan`): Customer Portal Data Plane (this repo).
- **`portalnoc`** (`https://github.com/raihanagilm/portalnoc`): Admin NOC Data Plane.
- **`portalvendor`** (`https://github.com/raihanagilm/portalvendor`): Vendor Control Plane managing multi-tenant ISP feature toggles (ON/OFF), subscription status, and theme policies.

## 2. Verification Commands
- Frontend build: `npm run build`
- Backend tests: `pytest tests/`

## 3. Hard Constraints & Commercial Guardrails
- **Zero NOC Admin Coupling:** Never import NOC admin modules (`app.modules.customers`, `app.modules.users`, `app.modules.settings`, `app.modules.activity_logs`, `scheduler_service`) into `portalpelanggan`.
- **Feature Guarding (Vendor Controlled):** Modules (`billing_va`, `quota_fup`, `wifi_management`, `connected_devices`, `speedtest`, `tickets`, `gps_lock`) must be gated on BOTH frontend navigation and backend FastAPI routes using signed policy from `portalvendor`.
- **White-Label Branding:** Theme colors come from Vendor policy (`portalvendor`), while the ISP brand **Logo & Name** come from local ISP configuration.
- **No Emoji / No Uncalibrated UI Slop:** Follow clean SVG icon standards and mobile-first ergonomics (375px+ baseline).
- **Security Boundaries:** Customer session cookies (`edtekno_pelanggan_session`) use isolated cryptographic salt; home-WiFi actions require `check_is_home_wifi` verification; billing/VA data must be read live from Network Bill API v1 without stale local caching beyond short request dedupe.

## 4. State Files
- `PROGRESS.md`: Current baseline, verified tests, and next steps.
- `DECISIONS.md`: Architectural Decision Records (ADR).
- `docs/architecture.md`: Fullstack layout and `portalvendor` policy integration flow.
