from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source="actor.username", read_only=True)
    recipient_username = serializers.CharField(source="recipient.username", read_only=True)
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ["id", "recipient", "recipient_username", "actor", "actor_username",
                  "verb", "target_repr", "created_at", "read"]
        read_only_fields = ["id", "recipient", "actor", "verb", "target_repr", "created_at"]

    def get_target_repr(self, obj):
        return str(obj.target) if obj.target else None
