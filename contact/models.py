"""
Model untuk aplikasi contact: pesan masuk dari formulir kontak.
"""

from django.db import models


class ContactMessage(models.Model):
    """Pesan yang dikirim pengunjung melalui formulir kontak."""

    name = models.CharField("nama", max_length=100)
    email = models.EmailField("email")
    subject = models.CharField("subjek", max_length=150)
    message = models.TextField("isi pesan")
    ip_address = models.GenericIPAddressField(
        "alamat IP", blank=True, null=True, editable=False
    )
    is_read = models.BooleanField("sudah dibaca", default=False)
    created_at = models.DateTimeField("diterima", auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Pesan Kontak"
        verbose_name_plural = "Pesan Kontak"
        indexes = (models.Index(fields=("is_read", "created_at")),)

    def __str__(self) -> str:
        return f"{self.subject} — {self.name}"