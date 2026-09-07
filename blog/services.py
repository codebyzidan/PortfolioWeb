"""
Service layer aplikasi blog.

Satu-satunya sumber query tulisan — views & app lain (core) memanggil
fungsi di sini, bukan membangun query sendiri.
"""

from __future__ import annotations

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from blog.models import Category, Post, Tag


def get_published_posts() -> models.QuerySet[Post]:
    """
    Tulisan terpublikasi, terbaru lebih dulu.

    `select_related` mencegah N+1 pada relasi author & category,
    `prefetch_related` mencegah N+1 saat tag dirender di tiap kartu.
    """
    return (
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .select_related("author", "category")
        .prefetch_related("tags")
    )


def get_latest_posts(limit: int = 3) -> models.QuerySet[Post]:
    """Tulisan terbaru untuk landing page."""
    return get_published_posts()[:limit]


def get_categories() -> models.QuerySet[Category]:
    """Semua kategori terurut abjad — untuk chip filter."""
    return Category.objects.all()


def get_tags() -> models.QuerySet[Tag]:
    """Semua tag terurut abjad — untuk chip filter."""
    return Tag.objects.all()


def get_visible_posts(user: AbstractBaseUser) -> models.QuerySet[Post]:
    """
    Queryset untuk halaman detail.

    Pengunjung umum hanya melihat tulisan terpublikasi; staff/superuser
    juga dapat membuka draft sebagai pratinjau.
    """
    queryset = (
        Post.objects.select_related("author", "category").prefetch_related("tags")
    )
    if user.is_staff:
        return queryset
    return queryset.filter(status=Post.Status.PUBLISHED)