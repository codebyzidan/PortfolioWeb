"""
Model untuk aplikasi projects: teknologi dan portofolio project.
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from core.validators import validate_image_upload


class Technology(models.Model):
    """Teknologi/perkakas yang digunakan pada project (badge & filter)."""

    name = models.CharField("nama", max_length=50, unique=True)
    slug = models.SlugField(
        "slug", max_length=60, unique=True, blank=True,
        help_text="Dibiarkan kosong = dibuat otomatis dari nama.",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Teknologi"
        verbose_name_plural = "Teknologi"

    def save(self, *args, **kwargs) -> None:
        """Membuat slug otomatis dari nama jika dibiarkan kosong."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    """Portofolio project yang ditampilkan di situs."""

    title = models.CharField("judul", max_length=120)
    slug = models.SlugField("slug", max_length=140, unique=True)
    summary = models.CharField(
        "ringkasan",
        max_length=200,
        help_text="1–2 kalimat untuk kartu project & meta description.",
    )
    description = models.TextField(
        "deskripsi",
        help_text=(
            "Penjelasan lengkap: latar belakang, peran Anda, solusi, dan hasil. "
            "Pisahkan paragraf dengan baris baru."
        ),
    )
    thumbnail = models.ImageField(
        "thumbnail",
        upload_to="projects/thumbnails/",
        blank=True,
        validators=[validate_image_upload],
        help_text="JPG/PNG/WebP, maksimal 2 MB.",
    )
    tech_stack = models.ManyToManyField(
        Technology,
        related_name="projects",
        blank=True,
        verbose_name="tech stack",
    )
    demo_url = models.URLField("tautan demo", blank=True)
    repo_url = models.URLField("tautan source code", blank=True)
    is_published = models.BooleanField("publikasikan", default=True)
    is_featured = models.BooleanField(
        "unggulan",
        default=False,
        help_text="Project unggulan tampil di landing page.",
    )
    order = models.PositiveSmallIntegerField(
        "urutan", default=0, help_text="Semakin kecil, semakin depan."
    )
    created_at = models.DateTimeField("dibuat", auto_now_add=True)
    updated_at = models.DateTimeField("diperbarui", auto_now=True)

    class Meta:
        ordering = ("order", "-created_at")
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def get_absolute_url(self) -> str:
        """URL detail project — dipakai template & admin."""
        return reverse("projects:detail", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return self.title