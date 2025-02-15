from rest_framework import viewsets, permissions
from marketplace.models import Notification
from marketplace.serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

# ✅ ViewSet for Managing Notifications
class NotificationViewSet(viewsets.ModelViewSet):
    """
    NotificationViewSet allows users to:
    - Retrieve their notifications.
    - Mark notifications as read.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication

    def get_queryset(self):
        """✅ Return notifications for the authenticated user"""
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['POST'])
    def mark_all_read(self, request):
        """✅ Mark all notifications as read"""
        self.get_queryset().update(is_read=True)
        return Response({"message": "All notifications marked as read."})
