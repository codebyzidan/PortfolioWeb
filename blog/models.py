"""
Model untuk aplikasi blog: kategori, tag, dan tulisan.
"""

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import Truncator, slugify

from core.validators import validate_image_upload


class Category(models.Model):
    """Kategori tulisan, mis. 'Tutorial' atau 'Catatan Belajar'."""

    name = models.CharField("nama", max_length=60, unique=True)
    slug = models.SlugField(
        "slug", max_length=70, unique=True, blank=True,
        help_text="Dibiarkan kosong = dibuat otomatis dari nama.",
    )
    description = models.TextField("deskripsi", blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Kategori"
        verbose_name_plural = "Kategori"

    def save(self, *args, **kwargs) -> None:
        """Membuat slug otomatis dari nama jika dibiarkan kosong."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    """Label fleksibel yang menandai topik sebuah tulisan."""

    name = models.CharField("nama", max_length=40, unique=True)
    slug = models.SlugField(
        "slug", max_length=50, unique=True, blank=True,
        help_text="Dibiarkan kosong = dibuat otomatis dari nama.",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Tag"
        verbose_name_plural = "Tag"

    def save(self, *args, **kwargs) -> None:
        """Membuat slug otomatis dari nama jika dibiarkan kosong."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    """Tulisan blog, ditulis dalam format Markdown."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Terpublikasi"

    title = models.CharField("judul", max_length=160)
    slug = models.SlugField("slug", max_length=180, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="blog_posts",
        editable=False,
        verbose_name="penulis",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="posts",
        verbose_name="kategori",
    )
    tags = models.ManyToManyField(
        Tag, related_name="posts", blank=True, verbose_name="tag"
    )
    cover_image = models.ImageField(
        "gambar sampul",
        upload_to="blog/covers/",
        blank=True,
        validators=[validate_image_upload],
        help_text="JPG/PNG/WebP, maksimal 2 MB.",
    )
    excerpt = models.CharField(
        "ringkasan",
        max_length=300,
        blank=True,
        help_text=(
            "1–2 kalimat untuk kartu & meta description. "
            "Dibiarkan kosong = digenerate otomatis dari isi."
        ),
    )
    content = models.TextField(
        "isi",
        help_text="Ditulis dengan format Markdown: heading, list, code block, tabel.",
    )
    status = models.CharField(
        "status", max_length=10, choices=Status.choices, default=Status.DRAFT
    )
    published_at = models.DateTimeField(
        "dipublikasikan", null=True, blank=True, editable=False
    )
    created_at = models.DateTimeField("dibuat", auto_now_add=True)
    updated_at = models.DateTimeField("diperbarui", auto_now=True)

    class Meta:
        ordering = ("-published_at", "-created_at")
        verbose_name = "Tulisan"
        verbose_name_plural = "Tulisan"
        indexes = (models.Index(fields=("status", "published_at")),)

    def save(self, *args, **kwargs) -> None:
        """Mengisi excerpt & published_at otomatis sesuai kondisi tulisan."""
        if not self.excerpt and self.content:
            self.excerpt = Truncator(self.content).words(24)
        if self.status == self.Status.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """URL detail tulisan — dipakai template & admin."""
        return reverse("blog:detail", kwargs={"slug": self.slug})

    @property
    def is_published(self) -> bool:
        """True jika tulisan sudah terpublikasi."""
        return self.status == self.Status.PUBLISHED

    @property
    def reading_time(self) -> int:
        """Estimasi waktu baca dalam menit (asumsi 200 kata/menit)."""
        return max(1, round(len(self.content.split()) / 200))

    def __str__(self) -> str:
        return self.title