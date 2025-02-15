from rest_framework import serializers
from .models import (
    CustomUser,
    VehicleBrand,
    VehicleModel,
    Vehicle,
    VehicleImage,
    VehicleFeature,
    VehicleFeaturesMapping,
    Chat,
    Message,
    Review,
    Notification,
    Favorite,
)


#  User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "phone_number", "last_seen"]


#  Vehicle Brand Serializer
class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = "__all__"


#  Vehicle Model Serializer
class VehicleModelSerializer(serializers.ModelSerializer):
    brand = VehicleBrandSerializer()  # Nested serialization

    class Meta:
        model = VehicleModel
        fields = "__all__"


#  Vehicle Image Serializer
class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ["id", "vehicle", "image"]


#  Vehicle Feature Serializer
class VehicleFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleFeature
        fields = "__all__"


#  Vehicle Features Mapping Serializer
class VehicleFeaturesMappingSerializer(serializers.ModelSerializer):
    feature = VehicleFeatureSerializer()

    class Meta:
        model = VehicleFeaturesMapping
        fields = ["id", "vehicle", "feature"]


#  Vehicle Serializer
class VehicleSerializer(serializers.ModelSerializer):
    seller = UserSerializer()  # Nested user data
    buyer = UserSerializer(allow_null=True)  # Buyer is optional
    model = VehicleModelSerializer()
    images = VehicleImageSerializer(many=True, read_only=True)
    vehicle_features = VehicleFeaturesMappingSerializer(many=True, read_only=True)

    class Meta:
        model = Vehicle
        fields = "__all__"


#  Chat Serializer
class ChatSerializer(serializers.ModelSerializer):
    buyer = UserSerializer()
    seller = UserSerializer()
    vehicle = VehicleSerializer()

    class Meta:
        model = Chat
        fields = "__all__"


#  Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()

    class Meta:
        model = Message
        fields = "__all__"


#  Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer()
    reviewed_user = UserSerializer()
    vehicle = VehicleSerializer()

    class Meta:
        model = Review
        fields = "__all__"


#  Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Notification
        fields = "__all__"


#  Favorite Serializer
class FavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    vehicle = VehicleSerializer()

    class Meta:
        model = Favorite
        fields = "__all__"
