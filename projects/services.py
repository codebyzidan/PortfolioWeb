"""
Service layer aplikasi projects.

Satu-satunya sumber query project — views & app lain (core) memanggil
fungsi di sini, bukan membangun query sendiri.
"""

from __future__ import annotations

from django.db import models

from projects.models import Project, Technology


def get_technologies() -> models.QuerySet[Technology]:
    """Semua teknologi terurut abjad — untuk chip filter halaman daftar."""
    return Technology.objects.all()


def get_published_projects() -> models.QuerySet[Project]:
    """
    Project terpublikasi, terurut sesuai field urutan lalu terbaru.

    `prefetch_related("tech_stack")` mencegah N+1 saat badge teknologi
    dirender di setiap kartu.
    """
    return (
        Project.objects.filter(is_published=True)
        .prefetch_related("tech_stack")
        .order_by("order", "-created_at")
    )


def get_featured_projects(limit: int | None = None) -> models.QuerySet[Project]:
    """Project unggulan untuk landing page; `limit` membatasi jumlahnya."""
    queryset = get_published_projects().filter(is_featured=True)
    return queryset[:limit] if limit else queryset


def get_published_project(slug: str) -> models.QuerySet[Project]:
    """Queryset project terpublikasi berdasarkan slug (untuk DetailView)."""
    return get_published_projects().filter(slug=slug)


def get_related_projects(project: Project, limit: int = 3) -> models.QuerySet[Project]:
    """Project terkait: memakai teknologi serupa, dikecualikan project ini."""
    return (
        get_published_projects()
        .filter(tech_stack__in=project.tech_stack.all())
        .exclude(pk=project.pk)
        .distinct()[:limit]
    )