from rest_framework import viewsets, permissions
from marketplace.models import Notification
from marketplace.serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


#   ViewSet for Managing Notifications
class NotificationViewSet(viewsets.ModelViewSet):
    """
    NotificationViewSet allows users to:
    - Retrieve their notifications.
    - Mark notifications as read.
    """

    queryset = Notification.objects.all()  #   ADDED queryset
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """  Retrieves only the authenticated user's notifications"""
        return Notification.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )

    @action(detail=False, methods=["POST"])
    def mark_all_read(self, request):
        """  Mark all notifications as read for the authenticated user"""
        Notification.objects.filter(user=request.user, is_read=False).update(
            is_read=True
        )
        return Response({"message": "All notifications marked as read."})
