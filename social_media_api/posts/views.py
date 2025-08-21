# posts/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework import permissions, filters
from django.contrib.auth import get_user_model
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

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
        serializer.save(author=self.request.user)


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
            Post.objects
            .filter(author__in=following_users)               # <-- Post.objects.filter(author__in=following_users)
            .select_related("author")
            .order_by("-created_at")                          # <-- .order_by
        )
