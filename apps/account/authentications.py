from django.contrib.auth.backends import BaseBackend
from apps.account.models import User


class CustomUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.get_by_username(username)
            if user and user.password == password:
                return user
        except:
            return None

    def get_user(self, user_id):
        try:
            return User.get(user_id)
        except:
            return None
