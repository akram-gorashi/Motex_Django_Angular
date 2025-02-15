from rest_framework import viewsets, permissions
from marketplace.models import Favorite
from marketplace.serializers import FavoriteSerializer

# ✅ ViewSet for Managing Favorites
class FavoriteViewSet(viewsets.ModelViewSet):
    """
    FavoriteViewSet allows users to:
    - Add vehicles to their favorites list.
    - Retrieve their list of favorite vehicles.
    - Remove vehicles from favorites.
    """
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication

    def get_queryset(self):
        """✅ Return only the authenticated user's favorite vehicles"""
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """✅ Auto-assigns the user when adding a favorite"""
        serializer.save(user=self.request.user)
