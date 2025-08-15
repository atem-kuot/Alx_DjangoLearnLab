from django.urls import path
from .views import UserLoginView, UserLogoutView, RegisterView, profile_view
from .views import (
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, PostDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    PostByTagListView, SearchView
    # plus your auth/profile views if you added them earlier
)

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", profile_view, name="profile"),
    # Posts
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    # Comments 
    path("post/<int:pk>/comments/new/", CommentCreateView.as_view(), name="comment-create"),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-edit"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
    # Tags
    path("tags/", PostByTagListView.as_view(), name="tags-list"),
    path("tags/<slug:tag_slug>/", PostByTagListView.as_view(), name="posts-by-tag"),
    path("search/", SearchView.as_view(), name="posts-search"),

]
