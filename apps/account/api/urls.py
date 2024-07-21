from django.urls import path
from apps.account.api.views import LoginAPIView, LogoutAPIView


urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
