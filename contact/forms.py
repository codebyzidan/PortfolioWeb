"""
Formulir untuk aplikasi contact.

Lapisan proteksi anti-spam/anti-bot pada level form:
1. Honeypot  — input tersembunyi yang harus kosong (jebakan bot sederhana).
2. Time-trap — token bertanda tangan kriptografis; kiriman yang terjadi
   kurang dari 2 detik sejak form dirender ditolak (manusia tidak mungkin,
   bot sangat mungkin). Tanda tangan mencegah pemalsuan nilai timestamp.
3. Batas panjang & minimal — mencegah pembengkakan data di database.
"""

import time

from django import forms
from django.core import signing

from contact.models import ContactMessage

FORM_TS_SALT = "contact.form_ts"
MIN_FILL_SECONDS = 2
MAX_FORM_AGE_SECONDS = 2 * 60 * 60  # token hangus setelah 2 jam
MAX_MESSAGE_LENGTH = 3000


class ContactForm(forms.ModelForm):
    """Formulir kontak pengunjung dengan proteksi berlapis."""

    honeypot = forms.CharField(
        required=False,
        label="Biarkan kosong",
        widget=forms.HiddenInput,
    )
    form_ts = forms.CharField(
        required=False,
        label="Waktu form dibuka",
        widget=forms.HiddenInput,
    )

    class Meta:
        model = ContactMessage
        fields = ("name", "email", "subject", "message")
        widgets = {
            "name": forms.TextInput(
                attrs={"autocomplete": "name", "placeholder": "Nama lengkap"}
            ),
            "email": forms.EmailInput(
                attrs={"autocomplete": "email", "placeholder": "nama@email.com"}
            ),
            "subject": forms.TextInput(attrs={"placeholder": "Subjek pesan"}),
            "message": forms.Textarea(
                attrs={"rows": 6, "placeholder": "Tulis pesan Anda di sini..."}
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        """Menyiapkan token time-trap untuk form yang belum dikirim."""
        super().__init__(*args, **kwargs)
        if not self.is_bound:
            self.initial["form_ts"] = signing.dumps(time.time(), salt=FORM_TS_SALT)

    def clean_honeypot(self) -> str:
        """Menolak kiriman yang mengisi honeypot (indikasi bot)."""
        value = self.cleaned_data.get("honeypot", "")
        if value:
            raise forms.ValidationError("Kiriman terdeteksi sebagai spam.")
        return value

    def clean_form_ts(self) -> str:
        """
        Memvalidasi token time-trap: asli (tanda tangan sah), belum hangus,
        dan diisi dalam durasi yang masuk akal bagi manusia.
        """
        raw = self.cleaned_data.get("form_ts", "")
        if not raw:
            raise forms.ValidationError(
                "Formulir tidak valid. Silakan muat ulang halaman."
            )
        try:
            rendered_at = float(
                signing.loads(raw, salt=FORM_TS_SALT, max_age=MAX_FORM_AGE_SECONDS)
            )
        except (signing.BadSignature, TypeError, ValueError):
            raise forms.ValidationError(
                "Sesi formulir sudah kedaluwarsa. Silakan muat ulang halaman."
            )
        if time.time() - rendered_at < MIN_FILL_SECONDS:
            raise forms.ValidationError(
                "Kiriman terdeteksi sebagai bot (terlalu cepat)."
            )
        return raw

    def clean_name(self) -> str:
        """Membersihkan dan memvalidasi panjang minimal nama."""
        value = self.cleaned_data["name"].strip()
        if len(value) < 2:
            raise forms.ValidationError("Nama terlalu pendek.")
        return value

    def clean_subject(self) -> str:
        """Membersihkan dan memvalidasi panjang minimal subjek."""
        value = self.cleaned_data["subject"].strip()
        if len(value) < 3:
            raise forms.ValidationError("Subjek terlalu pendek.")
        return value

    def clean_message(self) -> str:
        """Membatasi panjang isi pesan agar database tidak dibengkakkan."""
        value = self.cleaned_data["message"].strip()
        if len(value) < 10:
            raise forms.ValidationError("Pesan terlalu pendek (minimal 10 karakter).")
        if len(value) > MAX_MESSAGE_LENGTH:
            raise forms.ValidationError(
                f"Pesan maksimal {MAX_MESSAGE_LENGTH} karakter."
            )
        return value