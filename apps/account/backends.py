from django.contrib.auth.backends import BaseBackend
from apps.account.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CustomUserBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print('back')

        user = User.get_by_username(username)
        if user and user.password == password:
            return user
        return None

    def get_user(self, user_id):
        return User.get(user_id)


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            session_user = request.session['user']
            user = User.get(session_user['id'])
            if session_user['key'] == hash(user):
                user.is_authenticated = True
                return (user, None)

            return None
        except:
            return None

    def authenticate_header(self, request):
        return 'Bearer'
