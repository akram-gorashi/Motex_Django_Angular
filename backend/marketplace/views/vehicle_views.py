from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from marketplace.models import Vehicle
from marketplace.serializers import VehicleSerializer


#   Custom Pagination for Vehicles
class CustomPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = "page_size"  # Allow users to specify page size
    max_page_size = 50  # Maximum limit


#   Vehicle ViewSet - Handles all operations related to vehicles
class VehicleViewSet(viewsets.ModelViewSet):
    """
    VehicleViewSet allows users to:
    - Retrieve all public vehicle listings.
    - Create a new vehicle listing (only for authenticated users).
    - Update or delete a vehicle (only for the owner).
    - Filter, sort, and paginate vehicle listings.
    - Joins seller and brand in one query.
    - Prefetch related images & features
    """

    queryset = (
        Vehicle.objects.filter(is_active=True)
        .select_related("seller", "model__brand")
        .prefetch_related("images", "vehicle_features")
    )
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = [
        "model__brand__name",
        "model__name",
        "year",
        "fuel_type",
        "transmission",
        "price",
    ]
    ordering_fields = ["price", "year", "mileage"]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """  Assigns the authenticated user as the seller when a vehicle is created"""
        serializer.save(seller=self.request.user)

    def get_queryset(self):
        """  Return all public vehicles (does not filter by authenticated user)"""
        return Vehicle.objects.filter(is_active=True)

    @action(detail=True, methods=["POST"])
    def mark_sold(self, request, pk=None):
        """  Mark a vehicle as sold (only accessible to the seller)"""
        vehicle = self.get_object()
        vehicle.is_active = False
        vehicle.save()
        return Response({"message": "Vehicle marked as sold."})
