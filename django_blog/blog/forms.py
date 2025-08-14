from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile, Post, Comment


User = get_user_model()
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "profile_picture")


    tags_input = forms.CharField(
        required=False,
        help_text="Comma-separated tags, e.g. 'django, web, tips'"
    )

    class Meta:
        model = Post
        fields = ("title", "content", "tags_input")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Post title"}),
            "content": forms.Textarea(attrs={"rows": 8, "placeholder": "Write your post..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate tags_input when editing
        if self.instance and self.instance.pk:
            current = list(self.instance.tags.values_list("name", flat=True))
            if current:
                self.fields["tags_input"].initial = ", ".join(current)

    def clean_tags_input(self):
        # normalize user input (strip spaces, drop empties, de-duplicate case-insensitively)
        raw = self.cleaned_data.get("tags_input", "")
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        # make case-insensitive unique list but preserve original case of first occurrence
        seen_lower = set()
        unique = []
        for p in parts:
            key = p.lower()
            if key not in seen_lower:
                seen_lower.add(key)
                unique.append(p)
        return unique

class CommentForm(forms.ModelForm):
    """
    Used for creating/updating a comment.
    Author/post are set in the view; they are not user-editable here.
    """
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a comment..."}),
        }

    def clean_content(self):
        content = self.cleaned_data.get("content", "").strip()
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        return content
