"""
Konfigurasi admin untuk aplikasi blog.
"""

from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest

from blog.models import Category, Post, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin kategori tulisan."""

    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin tag tulisan."""

    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin tulisan: penulis diisi otomatis, status bisa diubah massal."""

    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    list_display = ("title", "category", "status", "published_at", "updated_at")
    list_filter = ("status", "category")
    search_fields = ("title", "excerpt", "content")
    date_hierarchy = "published_at"
    readonly_fields = ("created_at", "updated_at")
    actions = ("publish_posts", "unpublish_posts")
    fieldsets = (
        ("Identitas", {"fields": ("title", "slug")}),
        ("Konten", {"fields": ("category", "tags", "cover_image", "excerpt", "content")}),
        ("Publikasi", {"fields": ("status",)}),
        ("Metadata", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.action(description="Publikasikan tulisan terpilih")
    def publish_posts(self, request: HttpRequest, queryset: QuerySet[Post]) -> None:
        """Menandai tulisan terpilih sebagai terpublikasi (published_at terisi otomatis)."""
        for post in queryset:
            post.status = Post.Status.PUBLISHED
            post.save()
        self.message_user(
            request, f"{queryset.count()} tulisan dipublikasikan.", messages.SUCCESS
        )

    @admin.action(description="Jadikan draft tulisan terpilih")
    def unpublish_posts(self, request: HttpRequest, queryset: QuerySet[Post]) -> None:
        """Menarik tulisan terpilih kembali menjadi draft."""
        queryset.update(status=Post.Status.DRAFT)
        self.message_user(
            request, f"{queryset.count()} tulisan dijadikan draft.", messages.SUCCESS
        )

    def save_model(
        self,
        request: HttpRequest,
        obj: Post,
        form: any,
        change: bool,
    ) -> None:
        """Mengisi penulis secara otomatis dengan user yang sedang login."""
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)