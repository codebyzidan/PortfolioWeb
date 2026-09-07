"""
Model data konten utama portfolio: profil pemilik situs, keahlian, dan pengalaman.
"""

from django.db import models
from django.utils.formats import date_format

from core.validators import validate_document_upload, validate_image_upload


class Profile(models.Model):
    """
    Profil pemilik situs (pola singleton — selalu menggunakan baris pk=1).

    Menjadi sumber tunggal konten hero, tentang saya, dan kontak, sehingga
    perubahan konten cukup dilakukan lewat Django Admin tanpa edit kode.
    """

    full_name = models.CharField("nama lengkap", max_length=100)
    tagline = models.CharField(
        "tagline",
        max_length=120,
        help_text="Kalimat singkat peran/posisi. Contoh: Fullstack Developer — Django & TailwindCSS.",
    )
    intro = models.TextField(
        "intro hero",
        help_text="1–2 kalimat pembuka pada bagian hero.",
    )
    about = models.TextField(
        "tentang saya",
        help_text="Bio lengkap. Pisahkan paragraf dengan baris baru.",
    )
    photo = models.ImageField(
        "foto",
        upload_to="profile/",
        blank=True,
        validators=[validate_image_upload],
        help_text="JPG/PNG/WebP, maksimal 2 MB.",
    )
    cv_file = models.FileField(
        "file CV",
        upload_to="cv/",
        blank=True,
        validators=[validate_document_upload],
        help_text="PDF/DOC/DOCX, maksimal 5 MB.",
    )
    email = models.EmailField("email", blank=True)
    phone = models.CharField("telepon", max_length=20, blank=True)
    location = models.CharField(
        "lokasi", max_length=100, blank=True, help_text="Contoh: Jakarta, Indonesia"
    )
    open_to_work = models.BooleanField(
        "terbuka untuk peluang",
        default=True,
        help_text="Menampilkan badge status ketersediaan pada bagian hero.",
    )

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profil"

    def save(self, *args, **kwargs) -> None:
        """Memaksa pk=1 agar data profil selalu tunggal (singleton)."""
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.full_name or "Profil pemilik situs"


class SocialLink(models.Model):
    """Tautan media sosial milik profil."""

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="social_links"
    )
    label = models.CharField(
        "label",
        max_length=30,
        help_text="Nama platform. Contoh: GitHub, LinkedIn, Instagram, X, YouTube.",
    )
    url = models.URLField("tautan")
    order = models.PositiveSmallIntegerField("urutan", default=0)

    class Meta:
        ordering = ("order", "id")
        verbose_name = "Tautan Media Sosial"
        verbose_name_plural = "Tautan Media Sosial"

    def __str__(self) -> str:
        return self.label


class Skill(models.Model):
    """Keahlian teknis, dikelompokkan per kategori pada landing page."""

    class Category(models.TextChoices):
        BACKEND = "backend", "Backend"
        FRONTEND = "frontend", "Frontend"
        DATABASE = "database", "Database"
        TOOLS = "tools", "Tools & DevOps"
        OTHER = "other", "Lainnya"

    name = models.CharField("nama", max_length=50)
    category = models.CharField(
        "kategori", max_length=20, choices=Category.choices, default=Category.BACKEND
    )
    order = models.PositiveSmallIntegerField("urutan", default=0)

    class Meta:
        ordering = ("order", "name")
        verbose_name = "Keahlian"
        verbose_name_plural = "Keahlian"

    def __str__(self) -> str:
        return self.name


class Experience(models.Model):
    """Riwayat pekerjaan profesional untuk timeline pengalaman."""

    role = models.CharField("posisi", max_length=100)
    company = models.CharField("perusahaan/instansi", max_length=100)
    description = models.TextField(
        "deskripsi", blank=True, help_text="Poin pencapaian. Pisahkan dengan baris baru."
    )
    start_date = models.DateField("mulai")
    end_date = models.DateField(
        "selesai", null=True, blank=True, help_text="Kosongkan jika masih berjalan."
    )

    class Meta:
        ordering = ("-start_date",)
        verbose_name = "Pengalaman"
        verbose_name_plural = "Pengalaman"

    @property
    def is_current(self) -> bool:
        """True jika posisi masih berjalan (end_date kosong)."""
        return self.end_date is None

    @property
    def period(self) -> str:
        """Periode siap-tampil, mis. 'Jan 2023 — Sekarang' (terlokalisasi)."""
        start = date_format(self.start_date, "M Y")
        end = "Sekarang" if self.is_current else date_format(self.end_date, "M Y")
        return f"{start} — {end}"

    def __str__(self) -> str:
        return f"{self.role} @ {self.company}"