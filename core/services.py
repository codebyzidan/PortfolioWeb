"""
Service layer aplikasi core.

Menjadi satu-satunya sumber data konten untuk views, sehingga views tetap
ramping dan logika query tidak tersebar di banyak tempat.
"""

from __future__ import annotations

from django.db import models

from core.models import Experience, Profile, Skill

_PROFILE_DEFAULTS: dict = {
    "full_name": "Nama Anda",
    "tagline": "Fullstack Developer",
    "intro": "Perkenalkan diri Anda dalam 1–2 kalimat melalui Django Admin.",
}


def get_profile() -> Profile:
    """
    Mengembalikan profil pemilik situs (singleton pk=1).

    Menggunakan get_or_create agar situs tetap tampil walau admin belum
    pernah mengisi data; prefetch_related mencegah N+1 saat daftar tautan
    media sosial dirender di template.
    """
    profile, _ = Profile.objects.prefetch_related("social_links").get_or_create(
        pk=1, defaults=_PROFILE_DEFAULTS
    )
    return profile


def get_skill_groups() -> list[tuple[str, list[Skill]]]:
    """
    Mengembalikan daftar pasangan (nama kategori, daftar skill) yang sudah
    terurut sesuai field `order`, siap dirender sebagai grid per kategori.
    """
    groups: dict[str, list[Skill]] = {}
    for skill in Skill.objects.order_by("order", "name"):
        groups.setdefault(skill.get_category_display(), []).append(skill)
    return list(groups.items())


def get_experiences() -> models.QuerySet[Experience]:
    """Mengembalikan queryset pengalaman terurut dari yang terbaru."""
    return Experience.objects.all()