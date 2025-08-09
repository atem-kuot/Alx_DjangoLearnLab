from django.db import models
from django.utils import timezone

class Author(models.Model):
    """
    Represents a book author.
    One Author can have many Books.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book with a title, publication year, and an author.
    The 'author' field is a ForeignKey to Author (one-to-many).
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
