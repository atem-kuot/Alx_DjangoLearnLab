from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.generics import ListAPIView


class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD for posts.
    - Anyone can list/retrieve.
    - Only authenticated user can create.
    - Only author can update/delete.
    - Search by title/content/author username.
    - Ordering by created_at/updated_at/title.
    """
    queryset = Post.objects.all()
    queryset = Post.objects.select_related("author").all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
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
    - Ordering by created_at/updated_at.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = Comment.objects.all()
        qs = Comment.objects.select_related("author", "post").all().order_by("-created_at")
        post_id = self.request.query_params.get("post")
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class FeedView(ListAPIView):
    """
    GET: Personalized feed of posts by users that the current user follows.
    Ordered by newest first. Paginated by DRF defaults.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # user.following is available via related_name on the M2M in accounts.User
        followed_ids = user.following.values_list("id", flat=True)
        return (
            Post.objects
            .select_related("author")
            .filter(author_id__in=followed_ids)
            .order_by("-created_at")
        )
