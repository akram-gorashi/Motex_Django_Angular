from django.urls import path, include
from rest_framework.routers import DefaultRouter

from marketplace.views.brand_views import VehicleBrandViewSet
from marketplace.views.chat_views import ChatViewSet
from marketplace.views.favorite_views import FavoriteViewSet
from marketplace.views.message_views import MessageViewSet
from marketplace.views.model_views import VehicleModelViewSet
from marketplace.views.notification_views import NotificationViewSet
from marketplace.views.review_views import ReviewViewSet
from marketplace.views.user_views import UserViewSet
from marketplace.views.vehicle_views import VehicleViewSet


router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'brands', VehicleBrandViewSet)
router.register(r'models', VehicleModelViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
