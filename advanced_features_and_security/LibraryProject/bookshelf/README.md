## Groups & Permissions Setup

This application uses Django’s built-in groups and permissions to manage access to articles.

### Groups:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: All permissions including can_delete

### Permissions are enforced in views using:
@permission_required('news_app.can_<action>', raise_exception=True)

Assign users to groups in Django admin to grant appropriate access.
