"""
Views untuk aplikasi blog.
"""

from django.db import models
from django.views.generic import DetailView, ListView

from blog import services
from blog.models import Category, Tag


class PostListView(ListView):
    """
    Daftar tulisan terpublikasi.

    Mendukung filter kombinasi lewat query param:
    `?kategori=<slug>` dan `?tag=<slug>`. Filtering dilakukan di sisi
    server sehingga berfungsi tanpa JavaScript dan bisa di-bookmark.
    """

    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 8

    def get_queryset(self) -> models.QuerySet[models.Model]:
        """Mengambil tulisan terpublikasi dengan filter kategori/tag opsional."""
        queryset = services.get_published_posts()
        category_slug = self.request.GET.get("kategori", "")
        tag_slug = self.request.GET.get("tag", "")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        """Menambahkan daftar kategori/tag dan filter yang sedang aktif."""
        context = super().get_context_data(**kwargs)
        context["categories"] = services.get_categories()
        context["tags"] = services.get_tags()
        context["active_category"] = Category.objects.filter(
            slug=self.request.GET.get("kategori", "")
        ).first()
        context["active_tag"] = Tag.objects.filter(
            slug=self.request.GET.get("tag", "")
        ).first()
        return context


class PostDetailView(DetailView):
    """Halaman detail satu tulisan; staff dapat melihat pratinjau draft."""

    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self) -> models.QuerySet[models.Model]:
        """Draft hanya terlihat oleh staff — pengunjung umum mendapat 404."""
        return services.get_visible_posts(self.request.user)