# relationship_app/urls.py

from django.urls import path
from . import views
from .views import list_books, LibraryDetailView, RegisterView, UserLoginView, UserLogoutView


urlpatterns = [
    # Auth URLs
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # Book & Library Views
    path('books/', list_books, name='book_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
