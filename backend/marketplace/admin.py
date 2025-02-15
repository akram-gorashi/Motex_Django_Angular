from django.contrib import admin
from .models import (
    CustomUser, VehicleBrand, VehicleModel, Vehicle, 
    VehicleImage, VehicleFeature, VehicleFeaturesMapping, 
    Chat, Message, Review, Notification, Favorite
)

# ✅ Register User Model
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'last_seen', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('is_active', 'date_joined')
    ordering = ('-date_joined',)


# ✅ Register Vehicle Brand
@admin.register(VehicleBrand)
class VehicleBrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# ✅ Register Vehicle Model
@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'name')
    search_fields = ('name', 'brand__name')
    list_filter = ('brand',)


# ✅ Register Vehicle Model
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'buyer', 'model', 'year', 'price', 'is_active', 'created_at')
    search_fields = ('model__name', 'seller__username', 'vin')
    list_filter = ('is_active', 'year', 'price', 'fuel_type', 'transmission', 'condition')
    ordering = ('-created_at',)


# ✅ Register Vehicle Image
@admin.register(VehicleImage)
class VehicleImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'image')
    search_fields = ('vehicle__model__name',)


# ✅ Register Vehicle Feature
@admin.register(VehicleFeature)
class VehicleFeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# ✅ Register Vehicle Features Mapping
@admin.register(VehicleFeaturesMapping)
class VehicleFeaturesMappingAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'feature')
    search_fields = ('vehicle__model__name', 'feature__name')


# ✅ Register Chat
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'seller', 'vehicle', 'created_at')
    search_fields = ('buyer__username', 'seller__username', 'vehicle__model__name')


# ✅ Register Message
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'sender', 'message_text', 'sent_at')
    search_fields = ('chat__id', 'sender__username', 'message_text')


# ✅ Register Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'reviewer', 'reviewed_user', 'vehicle', 'rating', 'review_date')
    search_fields = ('reviewer__username', 'reviewed_user__username', 'vehicle__model__name')


# ✅ Register Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'notification_type', 'message', 'is_read', 'created_at')
    search_fields = ('user__username', 'notification_type', 'message')
    list_filter = ('is_read', 'notification_type')


# ✅ Register Favorite
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vehicle', 'created_at')
    search_fields = ('user__username', 'vehicle__model__name')
