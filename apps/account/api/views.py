from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from apps.account.api.serializers import UserSerializer
from django.contrib.auth import authenticate, logout
from drf_yasg.utils import swagger_auto_schema


class LoginAPIView(APIView):

    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        """
        User can login with this endpoint.
        params:
            - username: str
            - password: str
        """
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


class LogoutAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        """
        User can logout with this endpoint.
        """
        try:
            logout(request)
            return Response(
                {"message": "Successfully logged out"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": "unexpected error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
