"""
Konfigurasi URL untuk aplikasi projects.
"""

from django.urls import path

from projects import views

app_name = "projects"

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="list"),
    path("<slug:slug>/", views.ProjectDetailView.as_view(), name="detail"),
]