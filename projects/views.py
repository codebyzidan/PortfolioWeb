"""
Views untuk aplikasi projects.
"""

from django.db import models
from django.views.generic import DetailView, ListView

from projects import services
from projects.models import Technology


class ProjectListView(ListView):
    """
    Daftar seluruh project terpublikasi.

    Mendukung filter berdasarkan teknologi lewat query param `?tech=<slug>`.
    Filtering dilakukan di sisi server sehingga berfungsi tanpa JavaScript.
    """

    template_name = "projects/project_list.html"
    context_object_name = "projects"
    paginate_by = 9

    def get_queryset(self) -> models.QuerySet[models.Model]:
        """Mengambil project terpublikasi, difilter tech jika ada param."""
        queryset = services.get_published_projects()
        tech_slug = self.request.GET.get("tech", "")
        if tech_slug:
            queryset = queryset.filter(tech_stack__slug=tech_slug)
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        """Menambahkan daftar teknologi & teknologi aktif untuk chip filter."""
        context = super().get_context_data(**kwargs)
        context["technologies"] = services.get_technologies()
        context["active_tech"] = Technology.objects.filter(
            slug=self.request.GET.get("tech", "")
        ).first()
        return context


class ProjectDetailView(DetailView):
    """Halaman detail satu project + rekomendasi project terkait."""

    template_name = "projects/project_detail.html"
    context_object_name = "project"

    def get_queryset(self) -> models.QuerySet[models.Model]:
        """Hanya project terpublikasi — yang lain otomatis menghasilkan 404."""
        return services.get_published_projects()

    def get_context_data(self, **kwargs) -> dict:
        """Menambahkan project terkait berdasarkan kemiripan tech stack."""
        context = super().get_context_data(**kwargs)
        context["related_projects"] = services.get_related_projects(self.object)
        return context