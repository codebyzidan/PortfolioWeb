"""
Service layer aplikasi contact.
"""

from __future__ import annotations

from contact.models import ContactMessage


def create_message(
    *,
    name: str,
    email: str,
    subject: str,
    message: str,
    ip_address: str | None = None,
) -> ContactMessage:
    """
    Membuat pesan kontak baru dari data formulir yang sudah tervalidasi.

    Args:
        name: Nama pengirim.
        email: Email pengirim (untuk membalas).
        subject: Subjek pesan.
        message: Isi pesan.
        ip_address: IP pengirim untuk audit spam (opsional).
    """
    return ContactMessage.objects.create(
        name=name,
        email=email,
        subject=subject,
        message=message,
        ip_address=ip_address or None,
    )