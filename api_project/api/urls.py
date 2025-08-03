from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Original ListAPIView endpoint
    path('books/', BookList.as_view(), name='book-list'),
    path('auth-token/', obtain_auth_token, name='api_token_auth'),  
    # Include router URLs for CRUD operations
    path('', include(router.urls)),
]
