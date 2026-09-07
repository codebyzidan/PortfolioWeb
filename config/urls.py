"""
URL configuration utama proyek PortfolioWeb.

Path panel admin diambil dari `.env` (ADMIN_URL) agar dapat diubah
tanpa menyentuh kode — mengecoh bot yang memindai /admin/ secara otomatis.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include("core.urls")),
    path("projects/", include("projects.urls")),
    path("blog/", include("blog.urls")),
    path("contact/", include("contact.urls")),
]

# Sajikan file media saat development (DEBUG=True).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)