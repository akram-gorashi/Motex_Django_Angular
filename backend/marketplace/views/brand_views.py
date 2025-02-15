from rest_framework import viewsets, permissions
from marketplace.models import VehicleBrand
from marketplace.serializers import VehicleBrandSerializer

#   ViewSet for Vehicle Brands
class VehicleBrandViewSet(viewsets.ModelViewSet):
    """
    VehicleBrandViewSet allows:
    - Public retrieval of brands.
    - Admin users can add/edit/delete brands.
    """
    queryset = VehicleBrand.objects.all()
    serializer_class = VehicleBrandSerializer
    permission_classes = [permissions.AllowAny]  # Public access
