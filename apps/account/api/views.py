from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from apps.account.api.serializers import UserSerializer
from django.contrib.auth import authenticate, login
from hashlib import sha256


class LoginAPIView(APIView):
    """
    User can login with this endpoint.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            username = validated_data["username"]
            password = validated_data["password"]

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Successful authentication
                request.session["user"] = {"id": user.id, "key": hash(user)}
                # 1 hour user will be login
                request.session.set_expiry(60 * 60)

                return Response(
                    {"message": "Successfully logged in"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
