# ECOSYSTEM_SYNC.md : Kontrak Induk & Sinkronisasi Ekosistem 3-Repo

> **Master Source of Truth:** `portalvendor/ECOSYSTEM_SYNC.md` (`Contract Version: v1.1` | Diperbarui: `2026-11-26`)
>
> Berkas ini wajib dipertahankan **identik** di ketiga repositori berikut agar perubahan di satu tempat langsung terpantau di semua repo:
> 1. **`portalvendor`**: `d:\databaru\Magang\portalvendor\ECOSYSTEM_SYNC.md` (`https://github.com/raihanagilm/portalvendor`)
> 2. **`portalnoc`**: `d:\databaru\Magang\portalnoc\ECOSYSTEM_SYNC.md` (`https://github.com/raihanagilm/portalnoc`)
> 3. **`portalpelanggan`**: `d:\databaru\Magang\portalpelanggan\ECOSYSTEM_SYNC.md` (`https://github.com/raihanagilm/portalpelanggan`)

---

## 1. Aturan Sinkronisasi Lintas-Repo (Cross-Repo Doc Sync Protocol)

Karena `portalvendor`, `portalnoc`, dan `portalpelanggan` adalah tiga repositori Git terpisah, perubahan dokumentasi di satu repo tidak otomatis berubah di repo lain tanpa protokol disiplin:
1. **`portalvendor` adalah Master Contract:** Setiap perubahan arsitektur, pemetaan port, *feature keys*, payload *Signed Policy*, atau status milestone lintas-repo dimulai dari `portalvendor/ECOSYSTEM_SYNC.md`.
2. **Wajib Update Ketiga Repo:** Setiap developer atau AI Agent yang mengubah kontrak di salah satu repo wajib memperbarui `ECOSYSTEM_SYNC.md` dan `PROGRESS.md` di ketiga folder repositori pada sesi yang sama.
3. **Isolasi Web Produksi Live:** Web contoh yang sudah live (`https://portal.teknoindo.net/` dan `https://portal.teknoindo.net/portal/`) berjalan independen dan **tidak boleh disentuh langsung** saat pengembangan template/kontrol fitur di ketiga repositori ini.

---

## 2. Peta Repositori, Peran & Isolasi Blok Port

| Repositori | Peran dalam Ekosistem | Port Backend | Port Frontend Dev | Database (`.env`) | Keterangan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`portalvendor`** | **Control Plane (Vendor Only)** | **`9000`** *(FastAPI)* | **`5175`** *(Vite React)* | `portalvendor` *(MySQL :33070)* | Blok port terpisah jauh dari Data Plane. |
| **`portalnoc`** | **Data Plane Admin NOC** | `7890` *(FastAPI)* | `7891` *(Vite React)* | `edteknoguard` *(MySQL :33070)* | Template/deployment NOC per ISP (driver modem & VPN terisolasi). |
| **`portalpelanggan`** | **Data Plane Customer Portal** | `8001` *(FastAPI)* | `7891` *(Vite React)* | `edteknoguard` *(MySQL :33070)* | Template/deployment portal pelanggan mandiri per ISP. |

---

## 3. Spesifikasi Disepakati untuk `portalvendor` (Tahap 1)

1. **Gerbang Akses:** Wajib **Login Super Admin Vendor** di paling depan sebelum melihat daftar semua web ISP, info maintenance server, dan pengaturan fitur.
2. **Arah Visual UI:** **Light Mode bersih** (kartu putih, border tipis `slate-200`, token semantic, standar `antislop` diterapkan selama proses pengerjaan).
3. **Tata Letak Pusat Kendali Semua Web ISP (1 Kartu per Tenant ISP):**
   - Identitas & Status (`01. ISP-001`, nama ISP, status `ACTIVE` / `TRIAL` / `SUSPENDED`, masa aktif).
   - Tautan langsung ke aplikasi web ISP (`Buka NOC` misalnya `https://portal.teknoindo.net/` dan `Buka Portal` misalnya `https://portal.teknoindo.net/portal/`).
   - **Catatan Maintenance & Deployment** per web (`portalnoc` & `portalpelanggan`):
     - URL Repo Git & Branch (`repo_url`, `branch_name`)
     - Host/IP atau label VPS (`vps_host`)
     - User & Port SSH untuk perintah cepat copy-paste (`ssh_user`, `ssh_port`)
     - Path folder aplikasi di VPS (`vps_folder_path`)
     - Catatan teknis khusus ISP (perbedaan modem/VPN)
     - **Batasan Keamanan Mutlak:** Password SSH dan *private key* SSH dilarang disimpan di database/UI `portalvendor`.
   - Tombol **Kelola Fitur** untuk mengatur sakelar fitur `ON/OFF`, warna tema (`primary_color`, `accent_color`), dan menerbitkan *Signed Policy* `Ed25519`.
4. **Skema Database `portalvendor` (Bahasa Indonesia, 3NF, Structured Primary Key):**
   - `pengguna_vendor` (`id_pengguna` prefix `vndYYYYMMDDxxxx`)
   - `tenant_isp` (`id_tenant` prefix `ispYYYYMMDDxxxx`)
   - `deployment_tenant` (`id_deployment` prefix `depYYYYMMDDxxxx`, FK ke `tenant_isp`, per produk `portalnoc` / `portalpelanggan`)
   - `fitur_tenant` (`id_fitur` prefix `ftrYYYYMMDDxxxx`, FK ke `tenant_isp`)
   - `kebijakan_tenant` (`id_kebijakan` prefix `polYYYYMMDDxxxx`, FK ke `tenant_isp`)
   - `log_audit_kebijakan` (`id_audit` prefix `audYYYYMMDDxxxx`, FK ke `tenant_isp` & `pengguna_vendor`)

---

## 4. Kontrak *Signed Policy* & Feature Keys Kanonis (`Ed25519`)

- **Endpoint Control Plane:** `GET /api/v1/tenants/{tenant_id}/policy` (dilindungi `Authorization: Bearer <tenant_sync_token>`).
- **Penandatanganan:** Private Key `Ed25519` hanya berada di `portalvendor`; `portalnoc` dan `portalpelanggan` memverifikasi payload memakai Public Key `Ed25519` (diidentifikasi lewat `key_id`) dengan *grace period cache* (`expires_at`, default 24 jam).

### 4.1 Daftar Feature Keys `portalnoc`
| Feature Key | Target Backend (`portalnoc/routes/api.py`) | Target Frontend (`Navigation.jsx` / `App.jsx`) |
| :--- | :--- | :--- |
| `monitoring_ont` | `monitoring`, `optical_logs` | Tab `beranda`, `riwayat` |
| `mikrotik_sync` | `mikrotik` | Tab/aksi `mikrotik` |
| `billing_overview` | `billing` | Tab `pembayaran` |
| `quota_fup` | `quota` | Tab `kuota` |
| `tickets` | `tickets` | Tab `tiket` |
| `multi_office` | Endpoint manajemen cabang/kantor | Tab `manajemen-kantor`, `kantor` |
| `customer_logs` | `activity_logs` | Tab `log` |
| `push_notifications` | `notifications` | Lonceng & push notification |

*(Modul inti seperti `auth`, `dashboard` dasar, `customers` dasar, `users`, dan `settings` logo lokal tetap tersedia selama status tenant `ACTIVE` atau `TRIAL`.)*

### 4.2 Daftar Feature Keys `portalpelanggan`
| Feature Key | Target Backend (`app/portal/api_router.py`) | Target Frontend (`PortalNavigation.jsx` / `PortalCustomerApp.jsx`) |
| :--- | :--- | :--- |
| `dashboard_ont` | `dashboard` | Tab `beranda` |
| `billing_va` | `payment` | Tab `pembayaran` |
| `quota_fup` | `quota` | Tab `kuota` |
| `wifi_management` | `wifi` (ubah SSID & sandi) | Tab/menu `wifi` |
| `connected_devices` | `wifi` (daftar perangkat & blokir MAC) | Modal perangkat terhubung |
| `speedtest` | `speedtest` | Modal & endpoint speedtest |
| `tickets` | `tickets` | Tab `kendala` |
| `gps_lock` | `auth` / `profile` (sinkronisasi GPS otomatis) | Auto-lock koordinat rumah |

---

## 5. Rencana Tahap Pengerjaan & Daftar Refaktor Fitur Statik (Tahap 2)

### Tahap 1 : Pembangunan `portalvendor` (Fokus Berikutnya Setelah Review `.md`)
- [ ] Inisialisasi struktur modular FastAPI (`:9000`) + MySQL `portalvendor` + seeder `PT Tekno Indo Jaya`.
- [ ] Implementasi generator & signer `Ed25519` + CRUD `tenant_isp`, `deployment_tenant`, `fitur_tenant`, dan `log_audit_kebijakan`.
- [ ] Bangun UI Light Mode React + Vite (`:5175`): Login Vendor, Grid Kartu Web ISP + Catatan Maintenance (`Repo/VPS/SSH/Folder`), dan Drawer Kelola Fitur.

### Tahap 2 : Perbaikan Fitur Statik & Integrasi di `portalnoc` dan `portalpelanggan`
Saat ini di kedua repo Data Plane, daftar menu dan router API masih bersifat **statik (*hardcoded*)** sehingga belum bisa dimatikan/dinyalakan dari `portalvendor`. Pekerjaan perbaikan yang disiapkan di sana:

- **Daftar Tugas di `portalnoc`:**
  - [ ] Buat `app/core/feature_guard.py` untuk mengambil, memverifikasi tanda tangan `Ed25519`, dan men-cache policy dari `portalvendor` (mengembalikan `HTTP 403` jika fitur `false` atau tenant `suspended`).
  - [ ] Pasang dependency `require_feature("<key>")` pada router di `routes/api.py` dan `app/modules/*/routes.py`.
  - [ ] Tambahkan endpoint konfigurasi lokal (`GET /api/config/branding`) serta fitur upload **Logo & Nama Brand** lokal untuk Admin ISP di modul `settings`.
  - [ ] Refaktor `frontend/src/components/layout/Navigation.jsx` (`menuSections` yang saat ini `visible` statis, logo `/tekno-indo-logo.png`, nama `TeknoGuard`, dan warna hardcoded `#0B2545`) serta `frontend/src/App.jsx` agar dinamis mengikuti `features`, `theme`, dan `logo_url`.

- **Daftar Tugas di `portalpelanggan`:**
  - [ ] Buat `app/portal/core/feature_guard.py` untuk verifikasi `Ed25519` policy & `require_feature("<key>")`.
  - [ ] Pasang guard pada router di `app/portal/api_router.py` dan `app/portal/modules/*/routes.py`.
  - [ ] Tambahkan endpoint publik `GET /portal/api/config/branding` (menggabungkan `features` + `theme` dari `portalvendor` dengan `logo_url` + `brand_name` lokal).
  - [ ] Refaktor `src/portal/components/layout/PortalNavigation.jsx` (`PortalBottomNav` yang masih `grid-cols-5` statis dan `PortalNavbar` yang hardcode `TeknoCust` / `blue-600`) serta `src/portal/PortalCustomerApp.jsx` agar merender tab dan tema warna secara dinamis.

### Tahap 3 : Verifikasi End-to-End 3 Repo
- [ ] Uji toggle fitur ON/OFF dari `portalvendor` (`:5175`) hingga menu tersembunyi dan endpoint API mengembalikan `HTTP 403` di `portalnoc` (`:7890`) dan `portalpelanggan` (`:8001`), tanpa mengubah instance produksi `portal.teknoindo.net`.
