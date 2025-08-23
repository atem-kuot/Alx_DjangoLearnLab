from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework import generics, permissions, status
from .serializers import RegisterSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from notifications.utils import create_notification




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


#  User Login
class LoginView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
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


#  Profile View (authenticated users only)
class ProfileView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
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


class FollowUserView(APIView):
    """
    Allow the logged-in user to follow another user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # Ensure the target user exists
        target = get_object_or_404(CustomUser, id=user_id)

        # Prevent following yourself
        if target == request.user:
            return Response({"detail": "You cannot follow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Add target to current user's following set
        request.user.following.add(target)

        # Create a notification for the target
        create_notification(
            recipient=target,
            actor=request.user,
            verb="followed you"
        )

        return Response({"detail": f"You are now following {target.username}."},
                        status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    """
    Allow the logged-in user to unfollow another user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, id=user_id)

        if target == request.user:
            return Response({"detail": "You cannot unfollow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(target)

        return Response({"detail": f"You have unfollowed {target.username}."},
                        status=status.HTTP_200_OK)




