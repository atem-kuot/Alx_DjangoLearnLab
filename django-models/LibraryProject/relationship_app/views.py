
from django.shortcuts import render, get_object_or_404
from .models import Book, Library
from django.views.generic.detail import DetailView

def list_books(request):
    """Function-based view to list all books."""
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    """Class-based view to display details of a specific library."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
