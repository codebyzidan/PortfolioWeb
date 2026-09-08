"""
Pengaturan utama proyek PortfolioWeb.

Nilai sensitif dibaca dari file `.env` menggunakan django-environ.
Konfigurasi ini siap untuk development maupun production (cPanel/Passenger);
perbedaan perilaku dikendalikan sepenuhnya oleh variabel lingkungan.
"""

from datetime import timedelta
from pathlib import Path

import environ

# ---------------------------------------------------------------------------
# Path & Environment
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    CSRF_TRUSTED_ORIGINS=(list, []),
    ADMIN_URL=(str, "admin/"),
    SECURE_SSL_REDIRECT=(bool, False),
    SECURE_PROXY_SSL=(bool, False),
    SECURE_HSTS_SECONDS=(int, 0),
)

environ.Env.read_env(BASE_DIR / ".env")

# ---------------------------------------------------------------------------
# Inti Django
# ---------------------------------------------------------------------------
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
ADMIN_URL = env("ADMIN_URL")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

INSTALLED_APPS = [
    # Aplikasi bawaan Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Keamanan (brute-force protection)
    "axes",

    # Aplikasi lokal
    "accounts",
    "core",
    "projects",
    "blog",
    "contact",
]

MIDDLEWARE = [
    # Wajib paling atas: memblokir respons dari view yang terkunci oleh axes.
    "axes.middleware.AxesMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise: menyajikan file statis ter-kompresi dengan header cache permanen.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_profile",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ---------------------------------------------------------------------------
# Cache
# DatabaseCache dipakai karena Passenger menjalankan lebih dari satu proses;
# cache in-memory (LocMemCache) bersifat per-proses sehingga throttle kontak
# dan lockout axes tidak konsisten antar proses. Tabel cache dibuat via
# `createcachetable`.
# ---------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache",
    },
    "axes": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache",
    },
}

# ---------------------------------------------------------------------------
# Database (SQLite)
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ---------------------------------------------------------------------------
# Static & Storage
# WhiteNoise CompressedManifestStaticFilesStorage: gzip + nama file ber-hash
# (cache busting permanen). Wajib `collectstatic` setiap kali deploy.
# ---------------------------------------------------------------------------
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Batas global payload request (perlindungan DoS dasar).
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5 MB

# ---------------------------------------------------------------------------
# Autentikasi
# ---------------------------------------------------------------------------
AUTH_USER_MODEL = "accounts.User"

# Backend axes HARUS berada sebelum ModelBackend agar percobaan login
# diperiksa dulu terhadap status lockout.
AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]

AXES_CACHE = "axes"
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = timedelta(minutes=30)
AXES_RESET_ON_SUCCESS = True

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# Keamanan HTTP
# ---------------------------------------------------------------------------
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"

# HTTPS & cookie aman — diaktifkan lewat .env saat production (HTTPS sudah jalan).
SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT")
SESSION_COOKIE_SECURE = env("SECURE_SSL_REDIRECT")
CSRF_COOKIE_SECURE = env("SECURE_SSL_REDIRECT")
SECURE_HSTS_SECONDS = env("SECURE_HSTS_SECONDS")
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Hanya aktif jika aplikasi berada di balik proxy yang selalu menyetel
# header X-Forwarded-Proto (kondisi umum di cPanel dengan HTTPS).
if env("SECURE_PROXY_SSL"):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "id"
TIME_ZONE = "Asia/Jakarta"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Logging
# Error produksi (500, exception view) ditulis ke file di app root —
# tidak memerlukan konfigurasi SMTP dan tetap terekam walau pengunjung
# hanya melihat halaman 500 generik.
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} — {message}",
            "style": "{",
        },
    },
    "handlers": {
        "error_file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "error.log",
            "formatter": "verbose",
            "level": "ERROR",
            "delay": True,
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ("error_file",),
            "level": "ERROR",
            "propagate": False,
        },
    },
    "root": {"handlers": ("error_file",), "level": "WARNING"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"