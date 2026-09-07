"""
Konfigurasi admin untuk aplikasi accounts.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin kustom untuk model User.

    Mewarisi `UserAdmin` bawaan Django agar form create/change dan
    struktur fieldset tetap berfungsi penuh; hanya menyesuaikan kolom
    list dan pencarian.
    """

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)