from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # columns shown in the list
    list_filter = ('author', 'publication_year')            # sidebar filters
    search_fields = ('title', 'author')                     # search box


admin.site.register(Book)

