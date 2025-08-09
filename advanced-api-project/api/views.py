from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from django.utils import timezone


class BookListView(generics.ListAPIView):
    """
    GET: Retrieve a list of all books.
    Public access allowed (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can read
    # Enable filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering: exact matches
    filterset_fields = ['title', 'author__name', 'publication_year']

    # Searching: partial matches
    search_fields = ['title', 'author__name']

    # Ordering: specify sortable fields
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering


class BookDetailView(generics.RetrieveAPIView):
    """
    GET: Retrieve a single book by ID.
    Public access allowed (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can read


class BookCreateView(generics.CreateAPIView):
    """
    POST: Create a new book entry.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can create

    def perform_create(self, serializer):
        """
        Additional validation: Prevent creation of books in the future year.
        """
        year = serializer.validated_data.get('publication_year')
        if year > timezone.now().year:
            raise ValueError("Publication year cannot be in the future.")
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Update an existing book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can update

    def perform_update(self, serializer):
        year = serializer.validated_data.get('publication_year')
        if year > timezone.now().year:
            raise ValueError("Publication year cannot be in the future.")
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Remove a book entry.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can delete

