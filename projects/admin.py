"""
Konfigurasi admin untuk aplikasi projects.
"""

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from projects.models import Project, Technology


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    """Admin teknologi; slug otomatis dibuat dari nama jika kosong."""

    list_display = ("name", "slug")
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin project lengkap dengan aksi massal & kuration unggulan."""

    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tech_stack",)
    list_display = ("title", "is_published", "is_featured", "order", "created_at")
    list_editable = ("is_published", "is_featured", "order")
    list_filter = ("is_published", "is_featured", "tech_stack")
    search_fields = ("title", "summary")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    actions = ("make_published",)
    fieldsets = (
        ("Identitas", {"fields": ("title", "slug")}),
        ("Konten", {"fields": ("summary", "description", "thumbnail")}),
        ("Teknologi & Tautan", {"fields": ("tech_stack", "demo_url", "repo_url")}),
        ("Publikasi", {"fields": ("is_published", "is_featured", "order")}),
        ("Metadata", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.action(description="Publikasikan project terpilih")
    def make_published(self, request: HttpRequest, queryset: QuerySet[Project]) -> None:
        """Aksi massal: menandai project terpilih sebagai terpublikasi."""
        queryset.update(is_published=True)