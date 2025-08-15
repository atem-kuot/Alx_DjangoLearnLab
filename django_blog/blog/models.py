from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.text import slugify
from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = TaggableManager(blank=True)
    
    def __str__(self):
        return self.title

class Tag(models.Model):
    """
    Simple tag model. Tag names are unique.
    A slug is stored for clean URLs: /tags/<slug>/
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # ensure slug exists/updated if name changed
        if not self.slug:
            self.slug = slugify(self.name)
        else:
            # keep slugs stable; if you prefer auto-update, uncomment next line:
            # self.slug = slugify(self.name)
            pass
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True,null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)   


class Comment(models.Model):
    """
    Comment on a blog Post. Each comment belongs to one post and one user.
    """
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)   # first created
    updated_at = models.DateTimeField(auto_now=True)       # last edited

    class Meta:
        ordering = ['-created_at']  # newest first

    def __str__(self):
        return f'Comment by {self.author} on "{self.post}"'
