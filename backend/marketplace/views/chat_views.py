from rest_framework import viewsets, permissions
from marketplace.models import Chat
from marketplace.serializers import ChatSerializer

#   ViewSet for Managing Chat
class ChatViewSet(viewsets.ModelViewSet):
    """
    ChatViewSet allows users to:
    - Initiate and manage chats between buyers and sellers.
    """
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication

    def get_queryset(self):
        """  Return only chats involving the authenticated user"""
        return Chat.objects.filter(buyer=self.request.user) | Chat.objects.filter(seller=self.request.user)

    def perform_create(self, serializer):
        """  Auto-assign buyer when a chat is created"""
        serializer.save(buyer=self.request.user)
