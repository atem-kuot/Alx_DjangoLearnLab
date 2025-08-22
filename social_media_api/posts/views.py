# posts/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework import permissions, filters
from django.contrib.auth import get_user_model
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import IntegrityError
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from notifications.utils import create_notification





User = get_user_model()


class PostViewSet(ModelViewSet):
    """
    CRUD for posts.
    - Anyone can list/retrieve.
    - Only authenticated user can create.
    - Only author can update/delete.
    - Search by title/content/author username.
    - Ordering by created_at/updated_at/title.
    """
    queryset = Post.objects.select_related("author").all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content", "author__username"]
    ordering_fields = ["created_at", "updated_at", "title"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    """
    CRUD for comments.
    - Anyone can list/retrieve.
    - Only authenticated user can create.
    - Only comment author can update/delete.
    - Supports filtering by post via ?post=<post_id>
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = Comment.objects.select_related("author", "post").all().order_by("-created_at")
        post_id = self.request.query_params.get("post")
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        post_author = comment.post.author
        if post_author_id := getattr(post_author, "id", None):
            if post_author_id != self.request.user.id:
                create_notification(recipient=post_author, actor=self.request.user, verb="commented on your post", target=comment.post)

class FeedView(ListAPIView):
    """
    Personalized feed:
    Returns posts authored by users the current user follows,
    newest first. Requires authentication.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # users that the current user follows
        following_users = self.request.user.following.all()  # <-- following.all()
        # posts by followed users, newest first
        return (
            Post.objects.filter(author__in=following_users).order_by("-created_at")                          # <-- .order_by
        )


class PostViewSet(ModelViewSet):
    # ... (existing code unchanged)

    @action(detail=True, methods=["POST"], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        if post.author_id == request.user.id:
            # Allow liking your own post or block? Here we allow; change if needed.
            pass
        try:
            like = Like.objects.create(user=request.user, post=post)
        except IntegrityError:
            return Response({"detail": "Already liked."}, status=status.HTTP_200_OK)

        # Notify post author (avoid notifying self if you want)
        if post.author_id != request.user.id:
            create_notification(recipient=post.author, actor=request.user, verb="liked your post", target=post)

        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        if deleted:
            return Response({"detail": "Unliked."}, status=status.HTTP_200_OK)
        return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
