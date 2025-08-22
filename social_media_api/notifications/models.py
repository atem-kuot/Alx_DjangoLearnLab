from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

CustomUser = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(
        CustomUser,
        related_name="notifications",
        on_delete=models.CASCADE
    )
    actor = models.ForeignKey(
        CustomUser,
        related_name="notifications_from",
        on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=255)  # e.g., "liked your post", "followed you"

    # Generic relation to any target object (Post, Comment, etc.)
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("target_content_type", "target_object_id")

    # ✅ Add timestamp field
    timestamp = models.DateTimeField(auto_now_add=True)

    # Optional: mark notifications as read/unread
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient} - {self.verb}"
