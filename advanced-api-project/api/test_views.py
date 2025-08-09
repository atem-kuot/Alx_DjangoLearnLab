from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITests(APITestCase):
    """
    Test suite for Book API endpoints, including:
    - CRUD operations
    - Filtering, searching, ordering
    - Permissions
    """

    def setUp(self):
        # Create test user and authenticate
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()

        # Create authors and books
        self.author1 = Author.objects.create(name="Tolkien")
        self.author2 = Author.objects.create(name="Rowling")

        self.book1 = Book.objects.create(
            title="The Hobbit",
            publication_year=1937,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author2
        )

        self.list_url = reverse('book-list')  # Ensure your URL name matches in urls.py
        self.detail_url = reverse('book-detail', args=[self.book1.id])

    def test_list_books(self):
        """Test retrieving the list of books (public access)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_single_book(self):
        """Test retrieving a single book (public access)."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "The Hobbit")

    def test_create_book_authenticated(self):
        """Test creating a book as an authenticated user."""
        self.client.login(username="testuser", password="password123")
        payload = {
            "title": "The Lord of the Rings",
            "publication_year": 1954,
            "author": self.author1.id
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create a book."""
        payload = {
            "title": "The Silmarillion",
            "publication_year": 1977,
            "author": self.author1.id
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        """Test updating a book as an authenticated user."""
        self.client.login(username="testuser", password="password123")
        payload = {"title": "The Hobbit: Revised Edition"}
        response = self.client.patch(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "The Hobbit: Revised Edition")

    def test_delete_book_authenticated(self):
        """Test deleting a book as an authenticated user."""
        self.client.login(username="testuser", password="password123")
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_filter_books_by_author(self):
        """Test filtering books by author's name."""
        response = self.client.get(f"{self.list_url}?author__name=Tolkien")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "The Hobbit")

    def test_search_books(self):
        """Test searching books by keyword."""
        response = self.client.get(f"{self.list_url}?search=Harry")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Harry Potter and the Philosopher's Stone")

    def test_order_books_by_year_desc(self):
        """Test ordering books by publication_year descending."""
        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
