import unittest
from starlette.testclient import TestClient
from app.portal.main import app
from app.portal.core.security import create_customer_session_token, CUSTOMER_SESSION_COOKIE


class TestPortalSecurity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def setUp(self):
        self.client.cookies.clear()

    def test_security_headers_present(self):
        """Memastikan respons menyertakan header keamanan standar HTTP"""
        r = self.client.get("/portal/api/speedtest/ping")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers.get("x-content-type-options"), "nosniff")
        self.assertEqual(r.headers.get("x-frame-options"), "SAMEORIGIN")
        self.assertEqual(r.headers.get("x-xss-protection"), "1; mode=block")
        self.assertEqual(r.headers.get("referrer-policy"), "strict-origin-when-cross-origin")

    def test_mytekno_auth_rate_limiting(self):
        """Memastikan rate limiting melindungi reset password portal MyTekno"""
        test_ip = "192.0.2.100"
        client = TestClient(app, raise_server_exceptions=False)
        blocked = False
        for _ in range(15):
            res = client.post(
                "/portal/api/auth/minta-reset-password",
                json={"no_hp": "081234567890"},
                headers={"X-Forwarded-For": test_ip}
            )
            if res.status_code == 429:
                blocked = True
                break
        self.assertTrue(blocked, "Rate limiter harus memblokir flooding reset password MyTekno dengan HTTP 429.")

    def test_portal_register_fcm_rejects_unauthenticated_idor(self):
        """Memastikan /portal/api/auth/register-fcm menolak payload id_pelanggan tanpa cookie sesi"""
        r = self.client.post(
            "/portal/api/auth/register-fcm",
            json={"fcm_token": "fake_token_1234567890", "id_pelanggan": "CUST001", "kantor": "pusat"}
        )
        self.assertEqual(r.status_code, 401)

    def test_portal_reset_password_anti_enumeration(self):
        """Memastikan /portal/api/auth/minta-reset-password mengembalikan respons generik tanpa membocorkan nama/ID"""
        r = self.client.post(
            "/portal/api/auth/minta-reset-password",
            json={"no_hp": "089999999999"},
            headers={"X-Forwarded-For": "198.51.100.77"}
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertTrue(data.get("ok"))
        self.assertNotIn("nama", data)
        self.assertNotIn("id_pelanggan", data)

    def test_speedtest_download_upload_require_auth_and_cap_size(self):
        """Memastikan /speedtest/download & /upload mewajibkan login pelanggan dan membatasi ukuran upload"""
        self.client.cookies.clear()
        self.assertEqual(self.client.get("/portal/api/speedtest/download?bytes=1048576").status_code, 401)
        self.assertEqual(self.client.post("/portal/api/speedtest/upload", content=b"hello").status_code, 401)

        cust_token = create_customer_session_token(
            id_pelanggan="CUST-ST-01",
            nama="Speedtest User",
            status_verifikasi="TERVERIFIKASI",
            kantor="pusat"
        )
        self.client.cookies.set(CUSTOMER_SESSION_COOKIE, cust_token)

        r_ok = self.client.post("/portal/api/speedtest/upload", content=b"x" * 1024)
        self.assertEqual(r_ok.status_code, 200)
        self.assertTrue(r_ok.json().get("ok"))

        r_too_big = self.client.post("/portal/api/speedtest/upload", content=b"x" * (10 * 1024 * 1024 + 1024))
        self.assertEqual(r_too_big.status_code, 413)
