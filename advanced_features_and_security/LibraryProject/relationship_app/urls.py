# relationship_app/urls.py

from django.urls import path
from . import views
from .views import list_books, LibraryDetailView, admin_view, librarian_view, member_view,RegisterView, UserLoginView, UserLogoutView
from django.contrib.auth.views import LoginView, LogoutView
from relationship_app.views import book_permissions_views as book_views


urlpatterns = [
    # Auth URLs
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login')),
    path('logout/', LogoutView.as_view(template_name='logout')),

    # Book & Library Views
    path('books/', list_books, name='book_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    path('admin-only/', admin_view, name='admin_view'),
    path('librarian-only/', librarian_view, name='librarian_view'),
    path('member-only/', member_view, name='member_view'),


    path('add_book/', book_views.add_book, name='add_book'),
    path('edit_book/', book_views.edit_book, name='edit_book'),
    path('delete_book/', book_views.delete_book, name='delete_book'),
]

