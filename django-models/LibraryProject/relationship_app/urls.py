# relationship_app/urls.py

from django.urls import path
from . import views
from .views import list_books, LibraryDetailView, admin_view, librarian_view, member_view,RegisterView, UserLoginView, UserLogoutView
from django.contrib.auth.views import LoginView, LogoutView


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

]
