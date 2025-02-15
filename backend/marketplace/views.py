from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import (
    Chat,
    CustomUser,
    Favorite,
    Message,
    Notification,
    Review,
    Vehicle,
    VehicleBrand,
    VehicleFeature,
    VehicleFeaturesMapping,
    VehicleImage,
    VehicleModel,
)
from .serializers import (
    ChatSerializer,
    FavoriteSerializer,
    MessageSerializer,
    NotificationSerializer,
    ReviewSerializer,
    UserSerializer,
    VehicleBrandSerializer,
    VehicleFeatureSerializer,
    VehicleFeaturesMappingSerializer,
    VehicleImageSerializer,
    VehicleModelSerializer,
    VehicleSerializer,
)


#   Custom Pagination (Page Size = 10)
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


#  User ViewSet (Handles Users)
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


#  VehicleBrand ViewSet
class VehicleBrandViewSet(viewsets.ModelViewSet):
    queryset = VehicleBrand.objects.all()
    serializer_class = VehicleBrandSerializer
    permission_classes = [permissions.AllowAny]  # Public access


#  VehicleModel ViewSet
class VehicleModelViewSet(viewsets.ModelViewSet):
    queryset = VehicleModel.objects.all()
    serializer_class = VehicleModelSerializer
    permission_classes = [permissions.AllowAny]


#  Vehicle ViewSet (Handles Listings)
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = (
        Vehicle.objects.filter(is_active=True)
        .select_related("seller", "model__brand")
        .prefetch_related("images")
    )
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    #   Enable Filtering & Sorting
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
        serializer.save(
            seller=self.request.user
        )  # Auto-assign seller to logged-in user

    @action(detail=True, methods=["POST"])
    def mark_sold(self, request, pk=None):
        vehicle = self.get_object()
        vehicle.is_active = False  # Mark as sold
        vehicle.save()
        return Response({"message": "Vehicle marked as sold."})


#  Vehicle Image ViewSet
class VehicleImageViewSet(viewsets.ModelViewSet):
    queryset = VehicleImage.objects.all()
    serializer_class = VehicleImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


#  Vehicle Feature ViewSet
class VehicleFeatureViewSet(viewsets.ModelViewSet):
    queryset = VehicleFeature.objects.all()
    serializer_class = VehicleFeatureSerializer
    permission_classes = [permissions.AllowAny]


#  Chat ViewSet
class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)  # Auto-assign buyer


#  Message ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)  # Auto-assign sender


#  Review ViewSet
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]


#  Notification ViewSet
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]


#  Favorite ViewSet
class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Auto-assign logged-in user
