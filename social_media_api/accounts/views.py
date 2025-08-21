from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework import generics, permissions, status
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer

CustomUser = get_user_model()


#  User Registration
class RegisterView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()   # now includes CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "user": RegisterSerializer(user).data,
                "token": token.key,
            },
            status=status.HTTP_201_CREATED,
        )


# ✅ User Login
class LoginView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "user": RegisterSerializer(user).data,
                "token": token.key,
            },
            status=status.HTTP_200_OK,
        )


# ✅ Profile View (authenticated users only)
class ProfileView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
