"""
Model untuk aplikasi accounts.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User Model untuk seluruh proyek.

    Mewarisi `AbstractUser` agar seluruh fitur autentikasi bawaan Django
    tetap berfungsi, sekaligus memberi ruang penambahan field kustom di
    masa depan tanpa migrasi ulang.
    """

    email = models.EmailField(
        "email address",
        unique=True,
        help_text="Wajib diisi dan harus unik.",
        error_messages={"unique": "Email ini sudah terdaftar."},
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.username