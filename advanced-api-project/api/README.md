# API Endpoints for Books

- GET /api/books/ — List all books (public)
- GET /api/books/<id>/ — Retrieve a book by ID (public)
- POST /api/books/create/ — Create a new book (authenticated users only)
- PUT/PATCH /api/books/update/<id>/ — Update an existing book (authenticated)
- DELETE /api/books/delete/<id>/ — Delete a book (authenticated)

## Permissions
- Public read access for list & detail
- Create/Update/Delete require authentication
- Additional validation prevents books with a future publication year.

## Filtering
You can filter books by title, author name, and publication year:
  /api/books/?title=The Hobbit
  /api/books/?author__name=Tolkien
  /api/books/?publication_year=1937

## Searching
Search by partial matches in title or author name:
  /api/books/?search=Hobbit

## Ordering
Sort results by title or publication year:
  /api/books/?ordering=title
  /api/books/?ordering=-publication_year
