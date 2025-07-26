from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # columns shown in the list
    list_filter = ('author', 'publication_year')            # sidebar filters
    search_fields = ('title', 'author')                     # search box


admin.site.register(Book)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "date_of_birth", "profile_photo")}),
        (_("Permissions"), {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
        }),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "date_of_birth", "profile_photo"),
        }),
    )
    list_display = ("username", "email", "is_staff")
    search_fields = ("username", "email")
    ordering = ("username",)
