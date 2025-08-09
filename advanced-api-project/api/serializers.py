from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializes all fields of the Book model.
    Includes custom validation to prevent future publication years.
    """
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        """
        Ensure publication year is not in the future.
        """
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes the Author model, including a nested list of books.
    """
    books = BookSerializer(many=True, read_only=True)  # Nested representation

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
