from django.urls import path
from .views import UserLoginView, UserLogoutView, RegisterView, profile_view
from .views import (
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, PostDeleteView,
    # plus your auth/profile views if you added them earlier
)

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", profile_view, name="profile"),
    path("posts/", PostListView.as_view(), name="posts-list"),
    path("posts/new/", PostCreateView.as_view(), name="posts-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="posts-detail"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="posts-edit"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="posts-delete"),

]
