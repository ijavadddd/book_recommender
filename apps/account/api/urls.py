from django.urls import path
from apps.account.api.views import LoginAPIView


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
]
