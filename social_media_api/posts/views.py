# posts/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework import permissions, filters
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import IntegrityError
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework import permissions, filters, status, generics
from notifications.models import Notification


class PostViewSet(ModelViewSet):
    """
    CRUD for posts.
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

    @action(detail=True, methods=["POST"], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """
        Like a post:
        - Uses DRF generics.get_object_or_404 to fetch the post
        - Uses Like.objects.get_or_create to prevent duplicate likes
        - Creates a Notification directly via Notification.objects.create
        """
        post = generics.get_object_or_404(Post, pk=pk)  # <-- required
        like, created = Like.objects.get_or_create(      # <-- required
            user=request.user,
            post=post
        )
        if created:
            # notify the post author (avoid self-notify)
            if post.author_id != request.user.id:
                Notification.objects.create(            # <-- required
                    recipient=post.author,
                    actor=request.user,
                    verb="liked your post",
                    target=post
                )
            return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)
        return Response({"detail": "Already liked."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        """
        Unlike a post:
        - Uses DRF generics.get_object_or_404 to ensure the post exists
        """
        post = generics.get_object_or_404(Post, pk=pk)  # <-- required
        deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
        if deleted:
            return Response({"detail": "Unliked."}, status=status.HTTP_200_OK)
        return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(ModelViewSet):
    """
    CRUD for comments.
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
        # Notify post author on new comment (skip self)
        if comment.post.author_id != self.request.user.id:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb="commented on your post",
                target=comment.post
            )



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


