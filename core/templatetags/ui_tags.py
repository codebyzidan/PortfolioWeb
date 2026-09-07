"""
Template tags untuk kebutuhan UI lintas aplikasi.
"""

from django import template
from django.http import HttpRequest

register = template.Library()


@register.simple_tag(takes_context=True)
def nav_active(context: dict, app_name: str) -> str:
    """
    Mengembalikan kelas 'active' jika aplikasi yang sedang dibuka
    sama dengan `app_name`, selain itu string kosong.

    Dipakai pada link navbar untuk menandai halaman aktif,
    sehingga logika deteksi aktif hanya ditulis satu kali (DRY).
    """
    request: HttpRequest = context["request"]
    resolver = request.resolver_match
    if resolver is not None and resolver.app_name == app_name:
        return "active"
    return ""