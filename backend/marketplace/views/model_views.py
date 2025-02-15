from rest_framework import viewsets, permissions
from marketplace.models import VehicleModel
from marketplace.serializers import VehicleModelSerializer

# ✅ ViewSet for Vehicle Models
class VehicleModelViewSet(viewsets.ModelViewSet):
    """
    VehicleModelViewSet allows:
    - Public retrieval of vehicle models.
    - Admin users can add/edit/delete models.
    """
    queryset = VehicleModel.objects.all()
    serializer_class = VehicleModelSerializer
    permission_classes = [permissions.AllowAny]  # Public access
