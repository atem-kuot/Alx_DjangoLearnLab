from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    """
    List notifications for the current user.
    Unread first (see model Meta ordering), then newest first.
    Supports ?unread_only=true to filter.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Notification.objects.filter(recipient=self.request.user)
        if self.request.query_params.get("unread_only") in {"1", "true", "True"}:
            qs = qs.filter(read=False)
        return qs

class NotificationMarkReadView(generics.GenericAPIView):
    """
    Mark a single notification as read.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            notif = Notification.objects.get(pk=pk, recipient=request.user)
        except Notification.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        notif.read = True
        notif.save(update_fields=["read"])
        return Response(NotificationSerializer(notif).data)
