from django.urls import include, path
from rest_framework.routers import DefaultRouter

from test_app.views import UrlDetailView, UrlListView, create_short_url, redirect_to_url


app_name = "app"

urlpatterns = [
    path("urls/", UrlListView.as_view(), name="urls-list"),
    path("urls/<pk>/", UrlDetailView.as_view(), name="url-detail"),
    path("", create_short_url, name="create-url"),
    path("r/<enc_url>/", redirect_to_url, name="redirect-url"),
]
