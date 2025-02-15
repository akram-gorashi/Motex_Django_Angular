from rest_framework import viewsets, permissions
from marketplace.models import Review
from marketplace.serializers import ReviewSerializer

# ✅ ViewSet for Managing Reviews
class ReviewViewSet(viewsets.ModelViewSet):
    """
    ReviewViewSet allows users to:
    - Submit reviews for vehicles they have purchased.
    - View reviews submitted by other users.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Requires authentication

    def get_queryset(self):
        """✅ Return reviews written by the authenticated user"""
        return Review.objects.filter(reviewer=self.request.user)

    def perform_create(self, serializer):
        """✅ Auto-assign reviewer when a review is created"""
        serializer.save(reviewer=self.request.user)
