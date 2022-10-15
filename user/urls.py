from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import CreateUserView


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("access-token/", TokenObtainPairView.as_view(), name="access-token"),
    path("refresh-token/", TokenRefreshView.as_view(), name="refresh-token"),
]

app_name = "users"
