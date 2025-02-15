from django.contrib.auth.models import AbstractUser
from django.db import models


# ✅ Custom User Model (Extends Django's AbstractUser)
# - Represents sellers and buyers in the marketplace.
# - Users can sell vehicles, buy vehicles, write reviews, and receive notifications.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    last_seen = models.DateTimeField(
        auto_now=True
    )  # Tracks when the user was last active

    groups = models.ManyToManyField(
        "auth.Group", related_name="custom_user_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="custom_user_permissions", blank=True
    )

    def __str__(self):
        return self.username


# ✅ VehicleBrand Model (Previously "Make")
# - Represents a car manufacturer (e.g., Toyota, BMW, Ford).
# - A single brand can have multiple vehicle models.
class VehicleBrand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ✅ VehicleModel Model (Previously "Model")
# - Represents a specific car model belonging to a brand.
# - A single brand (VehicleBrand) can have multiple models.
class VehicleModel(models.Model):
    brand = models.ForeignKey(
        VehicleBrand, on_delete=models.CASCADE, related_name="models"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.brand.name} {self.name}"


# ✅ Vehicle Model
# - Each vehicle is linked to a seller (CustomUser).
# - A vehicle may have a buyer if it has been sold.
# - A vehicle belongs to a specific model (which in turn belongs to a brand).
class Vehicle(models.Model):
    seller = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="vehicles"
    )
    buyer = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="purchased_vehicles",
    )  # Protects buyer deletion

    model = models.ForeignKey(
        VehicleModel, on_delete=models.CASCADE, related_name="vehicles"
    )  # The model of the vehicle

    # Enum Choices for Consistent Data Entry
    class BodyType(models.TextChoices):
        SEDAN = "Sedan"
        SUV = "SUV"
        TRUCK = "Truck"
        COUPE = "Coupe"
        HATCHBACK = "Hatchback"
        CONVERTIBLE = "Convertible"

    class Condition(models.TextChoices):
        NEW = "New"
        USED = "Used"

    class Transmission(models.TextChoices):
        MANUAL = "Manual"
        AUTOMATIC = "Automatic"

    class FuelType(models.TextChoices):
        PETROL = "Petrol"
        DIESEL = "Diesel"
        ELECTRIC = "Electric"
        HYBRID = "Hybrid"

    body_type = models.CharField(max_length=20, choices=BodyType.choices)
    condition = models.CharField(max_length=10, choices=Condition.choices)
    transmission = models.CharField(max_length=10, choices=Transmission.choices)
    fuel_type = models.CharField(max_length=10, choices=FuelType.choices)

    mileage = models.IntegerField()
    price = models.IntegerField(db_index=True)  # Indexed for faster price filtering
    views = models.IntegerField(
        default=0, db_index=True
    )  # Indexed for popular listings
    year = models.IntegerField(db_index=True)

    color = models.CharField(max_length=50)
    vin = models.CharField(
        max_length=50, unique=True
    )  # Unique Vehicle Identification Number
    cylinders = models.IntegerField()
    engine_size = models.IntegerField()  # In cubic centimeters (cc)
    doors = models.IntegerField()
    description = models.TextField()
    location = models.CharField(max_length=255)
    vehicle_history = models.TextField()

    is_active = models.BooleanField(
        default=True
    )  # Soft delete instead of actual deletion
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model.brand.name} {self.model.name} ({self.year})"


# ✅ Vehicle Images
# - Each vehicle can have multiple images.
class VehicleImage(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="images"
    )  # One-to-Many: A vehicle can have multiple images
    image = models.ImageField(upload_to="vehicle_images/")

    def __str__(self):
        return f"Image for {self.vehicle.model.brand.name} {self.vehicle.model.name}"


# ✅ Vehicle Features
# - Represents features such as "Sunroof," "Bluetooth," "Leather Seats".
class VehicleFeature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ✅ Many-to-Many Relationship Between Vehicle & Features
class VehicleFeaturesMapping(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="vehicle_features"
    )
    feature = models.ForeignKey(VehicleFeature, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "vehicle",
            "feature",
        )  # Ensures a vehicle cannot have duplicate features

    def __str__(self):
        return f"{self.vehicle.model.brand.name} {self.vehicle.model.name} - {self.feature.name}"


# ✅ Favorite Model
# - Allows users to favorite vehicles.
# - A user can favorite multiple vehicles.
# - A vehicle can be favorited by multiple users.
class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="favorites"
    )  # The user who favorites the vehicle
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="favorited_by"
    )  # The vehicle being favorited
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Timestamp when the favorite was added

    class Meta:
        unique_together = (
            "user",
            "vehicle",
        )  # Ensures a user cannot favorite the same vehicle multiple times

    def __str__(self):
        return f"{self.user.username} favorited {self.vehicle.model.brand.name} {self.vehicle.model.name}"


# ✅ Chat Model
# - Represents a chat conversation between a buyer and seller about a vehicle.
class Chat(models.Model):
    buyer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="buyer_chats"
    )
    seller = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="seller_chats"
    )
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="chats")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.buyer.username} and {self.seller.username} for {self.vehicle.model.brand.name} {self.vehicle.model.name}"


# ✅ Message Model
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message_text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in chat {self.chat.id}"


# ✅ Review Model
# - A review is written by one user (Reviewer) for another user (Reviewed User) regarding a specific vehicle.
class Review(models.Model):
    reviewer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="written_reviews"
    )
    reviewed_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="received_reviews"
    )
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="reviews"
    )

    parent_review = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE
    )  # Enables replies to reviews

    rating = models.IntegerField()
    review_text = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewed_user.username} on {self.vehicle.model.brand.name} {self.vehicle.model.name}"


# ✅ Notification Model
# - Stores notifications for users.
class Notification(models.Model):
    class NotificationType(models.TextChoices):
        MESSAGE = "Message"
        VEHICLE_SOLD = "Vehicle Sold"
        PRICE_DROP = "Price Drop"

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="notifications"
    )
    notification_type = models.CharField(
        max_length=20, choices=NotificationType.choices
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"


""" 
 Entities & Relationships

CustomUser ↔ (1-to-Many) ↔ Car
Make ↔ (1-to-Many) ↔ CarModel
CarModel ↔ (1-to-Many) ↔ Car
Car ↔ (1-to-Many) ↔ Chat
Chat ↔ (1-to-Many) ↔ Message
User ↔ (Many-to-Many) ↔ Favorite Cars

"""
