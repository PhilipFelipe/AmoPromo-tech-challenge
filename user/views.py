from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserRegistrationView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username is already taken."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {"message": "User registered successfully.", "token": token.key},
            status=status.HTTP_201_CREATED,
        )
