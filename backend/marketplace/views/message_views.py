from rest_framework import viewsets, permissions
from marketplace.models import Message
from marketplace.serializers import MessageSerializer

# ✅ ViewSet for Managing Messages
class MessageViewSet(viewsets.ModelViewSet):
    """
    MessageViewSet allows users to:
    - Send and receive messages within chats.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication

    def get_queryset(self):
        """✅ Return messages sent by the authenticated user"""
        return Message.objects.filter(sender=self.request.user)

    def perform_create(self, serializer):
        """✅ Auto-assign sender when a message is created"""
        serializer.save(sender=self.request.user)
