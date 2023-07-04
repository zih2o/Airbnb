from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
import requests
from . import serializers
from .models import User


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.PrivateUserSerializer(request.user)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PrivateUserSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializers.PrivateUserSerializer(user).data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    def post(self, request):
        try:
            username = request.data.get("username")
            email = request.data.get("email")
            password = request.data.get("password")
            if not password:
                raise ParseError("password는 필수 입력값입니다.")
            if User.objects.filter(username=username).exists():
                return Response(
                    {"error": "This username already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if User.objects.filter(email=email).exists():
                return Response(
                    {"error": "This email already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = serializers.PrivateUserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.set_password(password)
                user.save()
                login(request, user)
                serializer = serializers.PrivateUserSerializer(user)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response({"error": "failed"}, status=status.HTTP_400_BAD_REQUEST)


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.PublicUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"ok": "login"})
        else:
            return Response(
                {"error": "username or password is not correct"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "logout"})


class GithubLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token?code={code}&client_id=024636271dcbf00c1fde&client_secret={settings.GH_SECRET}",
                headers={"Accept": "application/json"},
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()
            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_emails = user_emails.json()
            try:
                if user_emails[0].get("verified"):
                    user = User.objects.get(email=user_emails[0]["email"])
                    login(request, user)
                    return Response(status=status.HTTP_200_OK)
                else:
                    raise ParseError("유효하지 않은 이메일입니다.")
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login"),
                    name=user_data.get("name"),
                    email=user_emails[0]["email"],
                    avatar=user_data.get("avatar_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class KakaoLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": "3578cdbb0e21d6feabaa9d424e7d14e5",
                    "redirect_uri": f"{settings.FRONTEND_HOST}/social/kakao",
                    "code": code,
                },
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                if kakao_account.get("is_email_verified"):
                    user = User.objects.get(email=kakao_account.get("email"))
                    login(request, user)
                    return Response(status=status.HTTP_200_OK)
                else:
                    raise ParseError("유효하지 않은 이메일입니다.")
            except User.DoesNotExist:
                user = User.objects.create(
                    username=profile.get("nickname"),
                    name=profile.get("nickname"),
                    email=kakao_account.get("email"),
                    avatar=profile.get("thumbnail_image_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
