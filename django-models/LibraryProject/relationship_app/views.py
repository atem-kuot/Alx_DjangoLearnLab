
from django.shortcuts import render, redirect
from .models import Library, Book
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login


def list_books(request):
    """Function-based view to list all books."""
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    """Class-based view to display details of a specific library."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

from django.shortcuts import render, redirect
from django.views import View

# Registration View
class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in
            return redirect('book_list')  # Redirect to book list or home
        return render(request, 'relationship_app/register.html', {'form': form})

# Login View (uses built-in LoginView)
class UserLoginView(LoginView):
    template_name = 'relationship_app/login.html'

# Logout View (uses built-in LogoutView)
class UserLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'
