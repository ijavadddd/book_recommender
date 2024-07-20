from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import connection
from apps.account.api.serializers import UserSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY, get_backends
from hashlib import sha256


class LoginAPIView(APIView):
    """
    user could login with this endpoint
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            params = [validated_data['username'], validated_data['password']]
            # Open a cursor to perform database operations
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                # Fetch all results from the executed query
                result = cursor.fetchone()
                user = authenticate(request, username=result[1], password=result[2])
                if user is not None:
                    request.session[SESSION_KEY] = user.id
                    request.session[BACKEND_SESSION_KEY] = 'apps.account.authentications.CustomUserBackend',
                    request.session[HASH_SESSION_KEY] = sha256(user.password.encode('utf-8')).hexdigest()
                    return Response({"message": "successfully login"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

