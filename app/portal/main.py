import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.middleware.security_middleware import SecurityHeadersMiddleware, LoginRateLimitMiddleware
from app.portal.api_router import api_router as portal_api_router
from app.portal.core.security import (
    get_current_customer_optional,
    create_customer_session_token,
    CUSTOMER_SESSION_COOKIE,
    MAX_SESSION_AGE,
)

app = FastAPI(
    title="MyTekno — Portal Layanan Pelanggan",
    description="Aplikasi Layanan Mandiri & Lapor Kendala Pelanggan Internet",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(LoginRateLimitMiddleware, max_attempts=10, window_seconds=60)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Active-Kantor", "X-Client-SSID", "X-Client-Gateway-MAC"],
)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 303 and exc.headers and "Location" in exc.headers:
        return RedirectResponse(url=exc.headers["Location"], status_code=303)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.middleware("http")
async def customer_session_middleware(request: Request, call_next):
    cust = get_current_customer_optional(request)
    request.state.current_customer = cust
    response = await call_next(request)

    path_lower = request.url.path.lower().rstrip("/")
    is_auth_or_static = (
        path_lower.endswith("/logout")
        or path_lower.endswith("/login")
        or path_lower.endswith("/daftar")
        or request.url.path.startswith("/static")
        or "/static" in path_lower
    )

    if cust and request.method == "GET" and not is_auth_or_static:
        refreshed_token = create_customer_session_token(
            id_pelanggan=cust.get("id_pelanggan", ""),
            nama=cust.get("nama", ""),
            status_verifikasi=cust.get("status_verifikasi", ""),
            kantor=cust.get("kantor", ""),
        )
        from app.core.security import is_https_request
        response.set_cookie(
            key=CUSTOMER_SESSION_COOKIE,
            value=refreshed_token,
            max_age=MAX_SESSION_AGE,
            httponly=True,
            samesite="lax",
            secure=is_https_request(request),
            path="/",
        )
    return response


static_dir = Path("static")
static_dir.mkdir(parents=True, exist_ok=True)
(static_dir / "uploads" / "profil").mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="portal_static")

dist_dir = Path("dist")
if dist_dir.exists() and (dist_dir / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(dist_dir / "assets")), name="portal_assets")

mascots_dir = (dist_dir / "mascots") if (dist_dir / "mascots").exists() else Path("public/mascots")
if mascots_dir.exists():
    app.mount("/mascots", StaticFiles(directory=str(mascots_dir)), name="portal_mascots")


@app.get("/frame-36.png")
@app.get("/favicon.svg")
@app.get("/favicon.png")
@app.get("/icons.svg")
@app.get("/tekno-indo-logo.png")
@app.get("/tekno_indo_logo.png")
@app.get("/teknocust-mascot.png")
def serve_root_static_files(request: Request):
    filename = request.url.path.lstrip("/")
    for base in (dist_dir, Path("public")):
        target = base / filename
        if not target.exists() and filename == "tekno_indo_logo.png":
            target = base / "tekno-indo-logo.png"
        if target.exists() and target.is_file():
            return FileResponse(str(target))
    return JSONResponse(status_code=404, content={"detail": f"{filename} not found"})


# Registrasi Router API REST Portal Pelanggan (/portal/api/...)
app.include_router(portal_api_router, prefix="/portal")

DIST_INDEX = dist_dir / "index.html"


@app.get("/{full_path:path}")
def serve_portal_spa(request: Request, full_path: str = ""):
    if DIST_INDEX.exists():
        return FileResponse(
            str(DIST_INDEX),
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            },
        )
    return JSONResponse(
        status_code=404,
        content={"error": "Frontend dist belum dibuild. Jalankan 'npm run build' di root portalpelanggan."},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.portal.main:app", host="0.0.0.0", port=settings.APP_PORT, reload=True)
