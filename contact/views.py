"""
Views untuk aplikasi contact.
"""

from django.contrib import messages
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from contact import services
from contact.forms import ContactForm

# Jeda minimum antar kiriman dari IP yang sama (detik).
RATE_LIMIT_SECONDS = 60


class ContactView(FormView):
    """
    Halaman formulir kontak.

    Proteksi berlapis tanpa dependensi eksternal:
    1. Honeypot & time-trap (di ContactForm) — menggagalkan bot.
    2. Throttle per-IP via cache — membatasi frekuensi kiriman, tetap
       bekerja walau klien tidak menyimpan cookie (lebih kuat daripada
       throttle berbasis session).
    """

    form_class = ContactForm
    template_name = "contact/contact.html"
    success_url = reverse_lazy("contact:index")

    def get_initial(self) -> dict:
        """Prefill nama & email jika pengunjung sudah login."""
        initial = super().get_initial()
        user = self.request.user
        if user.is_authenticated:
            initial["name"] = user.get_full_name() or user.username
            initial["email"] = user.email
        return initial

    def form_valid(self, form: ContactForm) -> HttpResponse:
        """Menyimpan pesan lewat service layer dengan throttle per-IP."""
        ip_address = self.get_client_ip(self.request) or "unknown"
        throttle_key = f"contact:rl:{ip_address}"

        if cache.get(throttle_key):
            form.add_error(
                None,
                "Terlalu banyak pesan dikirim dari perangkat Anda. "
                "Silakan coba lagi satu menit lagi.",
            )
            return self.form_invalid(form)

        data = form.cleaned_data
        services.create_message(
            name=data["name"],
            email=data["email"],
            subject=data["subject"],
            message=data["message"],
            ip_address=self.get_client_ip(self.request),
        )
        cache.set(throttle_key, 1, timeout=RATE_LIMIT_SECONDS)

        messages.success(
            self.request,
            "Terima kasih! Pesan Anda sudah terkirim dan akan segera saya baca.",
        )
        return super().form_valid(form)

    @staticmethod
    def get_client_ip(request: HttpRequest) -> str | None:
        """
        Mengambil IP pengunjung.

        Mengutamakan `X-Forwarded-For` (kondisi di balik reverse proxy
        seperti cPanel/LiteSpeed), mengambil alamat pertama dalam daftar.
        Catatan: header ini dapat dipalsukan klien, sehingga nilai ini
        hanya untuk audit & throttle best-effort, bukan kontrol keamanan.
        """
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")