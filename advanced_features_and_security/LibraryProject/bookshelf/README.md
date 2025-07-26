## User Roles & Permissions Setup

This app uses Django's group and permission system to manage access to the `Book` model.

### Custom Permissions (in Book model):
- `can_view`: Can view book list
- `can_create`: Can create a new book
- `can_edit`: Can edit an existing book
- `can_delete`: Can delete a book

### User Groups:
- **Viewers**: can_view
- **Editors**: can_create, can_edit
- **Admins**: All permissions

To set up the groups and permissions automatically, run:

