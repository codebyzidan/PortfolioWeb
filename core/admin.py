"""
Konfigurasi admin untuk aplikasi core.
"""

from django.contrib import admin
from django.http import HttpRequest

from core.models import Experience, Profile, Skill, SocialLink


class SocialLinkInline(admin.TabularInline):
    """Inline untuk mengelola tautan sosial langsung dari halaman Profil."""

    model = SocialLink
    extra = 2


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin profil (singleton): hanya satu baris yang boleh ada."""

    fieldsets = (
        ("Identitas", {"fields": ("full_name", "tagline", "intro")}),
        ("Bio & Media", {"fields": ("about", "photo", "cv_file")}),
        ("Kontak & Status", {"fields": ("email", "phone", "location", "open_to_work")}),
    )
    inlines = (SocialLinkInline,)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Blokir pembuatan baris kedua (singleton)."""
        return not Profile.objects.exists()

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        """Profil tidak boleh dihapus dari admin."""
        return False


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order")
    list_editable = ("order",)
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "start_date", "end_date", "is_current")
    search_fields = ("role", "company")