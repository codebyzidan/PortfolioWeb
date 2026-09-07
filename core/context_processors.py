"""
Context processor aplikasi core.

Menyuntikkan data lintas-halaman (profil pemilik situs) ke seluruh template,
sehingga navbar, footer, dan section lain tidak perlu mengirim ulang data
dari setiap view (prinsip DRY).
"""

from django.http import HttpRequest

from core import services


def site_profile(request: HttpRequest) -> dict:
    """Menyediakan variabel `site_profile` ke semua template."""
    return {"site_profile": services.get_profile()}