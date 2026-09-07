"""
Views untuk aplikasi core.
"""

from django.views.generic import TemplateView

from blog import services as blog_services
from core import services
from projects import services as project_services


class HomeView(TemplateView):
    """
    Landing page portfolio.

    Context `site_profile` disediakan otomatis oleh context processor;
    data section lainnya diambil dari service layer masing-masing app.
    """

    template_name = "core/home.html"

    def get_context_data(self, **kwargs) -> dict:
        """Menggabungkan data dari service layer core, projects, dan blog."""
        context = super().get_context_data(**kwargs)
        context["skill_groups"] = services.get_skill_groups()
        context["experiences"] = services.get_experiences()
        context["featured_projects"] = project_services.get_featured_projects(limit=3)
        context["latest_posts"] = blog_services.get_latest_posts(limit=3)
        return context