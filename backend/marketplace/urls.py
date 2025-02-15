from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, VehicleBrandViewSet, VehicleModelViewSet, VehicleViewSet, 
    VehicleImageViewSet, VehicleFeatureViewSet, ChatViewSet, MessageViewSet, 
    ReviewViewSet, NotificationViewSet, FavoriteViewSet
)

#  Register ViewSets with Router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'vehicle-brands', VehicleBrandViewSet, basename='vehiclebrand')
router.register(r'vehicle-models', VehicleModelViewSet, basename='vehiclemodel')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'vehicle-images', VehicleImageViewSet, basename='vehicleimage')
router.register(r'vehicle-features', VehicleFeatureViewSet, basename='vehiclefeature')
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'favorites', FavoriteViewSet, basename='favorite')

#  API URL Patterns
urlpatterns = [
    path('api/', include(router.urls)),
]
