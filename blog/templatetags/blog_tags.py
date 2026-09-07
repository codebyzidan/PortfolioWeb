"""
Template tags & filters untuk aplikasi blog.
"""

import mistune
from django import template
from django.utils.safestring import SafeString, mark_safe

register = template.Library()

_markdown = mistune.create_markdown(
    plugins=["table", "strikethrough", "task_lists"]
)


@register.filter
def render_markdown(value: str) -> SafeString:
    """
    Mengonversi teks Markdown menjadi HTML.

    Raw HTML di dalam konten otomatis di-escape oleh mistune. Konten hanya
    ditulis pemilik situs melalui Django Admin, sehingga hasil render
    dianggap tepercaya dan ditandai safe.
    """
    return mark_safe(_markdown(value or ""))