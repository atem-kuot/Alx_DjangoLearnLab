from rest_framework import viewsets, ModelViewSet
from .models import Book    
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class BookList (viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'destroy':  # DELETE method
            return [IsAdminUser()]
        return [IsAuthenticated()]

    