"""
Konfigurasi admin untuk aplikasi contact.
"""

from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest

from contact.models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Inbox pesan kontak: hanya membaca & menandai status dibaca."""

    list_display = ("subject", "name", "email", "is_read", "created_at")
    list_editable = ("is_read",)
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    date_hierarchy = "created_at"
    readonly_fields = ("name", "email", "subject", "message", "ip_address", "created_at")
    actions = ("mark_as_read", "mark_as_unread")
    fieldsets = (
        ("Pesan", {"fields": ("name", "email", "subject", "message")}),
        ("Metadata", {"fields": ("is_read", "ip_address", "created_at")}),
    )

    @admin.action(description="Tandai sudah dibaca")
    def mark_as_read(self, request: HttpRequest, queryset: QuerySet[ContactMessage]) -> None:
        """Menandai pesan terpilih sebagai sudah dibaca."""
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} pesan ditandai sudah dibaca.", messages.SUCCESS)

    @admin.action(description="Tandai belum dibaca")
    def mark_as_unread(self, request: HttpRequest, queryset: QuerySet[ContactMessage]) -> None:
        """Menandai pesan terpilih sebagai belum dibaca."""
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} pesan ditandai belum dibaca.", messages.SUCCESS)

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Pesan hanya boleh masuk lewat formulir kontak, bukan admin."""
        return False