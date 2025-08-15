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


class PostForm(forms.ModelForm):
    """
    Author is set in the view; not user-editable here.
    'tags' is provided by django-taggit and accepts comma-separated input.
    """
    class Meta:
        model = Post
        fields = ("title", "content", "tags")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Post title"}),
            "content": forms.Textarea(attrs={"rows": 8, "placeholder": "Write your post..."}),
        }

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
