"""
Konfigurasi URL untuk aplikasi blog.
"""

from django.urls import path

from blog import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="list"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="detail"),
]