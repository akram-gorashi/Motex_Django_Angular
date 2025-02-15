from django.db import models
from django.contrib.auth import get_user_model
from marketplace.enums.vehicle_enum import BodyType, Condition, Transmission, FuelType

User = get_user_model()

class VehicleBrand(models.Model):
    """  Represents vehicle brands (e.g., Toyota, BMW)"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class VehicleModel(models.Model):
    """  Represents vehicle models under a brand (e.g., Corolla, Mustang)"""
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.brand.name} {self.name}"

class Vehicle(models.Model):
    """  Represents a vehicle listing with seller, buyer, and specifications"""
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicles")
    buyer = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name="purchased_vehicles")

    model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, related_name="vehicles")
    body_type = models.CharField(max_length=20, choices=BodyType.choices())
    transmission = models.CharField(max_length=20, choices=Transmission.choices())
    fuel_type = models.CharField(max_length=20, choices=FuelType.choices())

    mileage = models.IntegerField()
    price = models.IntegerField(db_index=True)
    views = models.IntegerField(default=0, db_index=True)
    year = models.IntegerField(db_index=True)
    color = models.CharField(max_length=50)
    vin = models.CharField(max_length=50, unique=True)
    cylinders = models.IntegerField()
    engine_size = models.IntegerField()
    doors = models.IntegerField()
    description = models.TextField()
    location = models.CharField(max_length=255)
    vehicle_history = models.TextField()
    condition = models.CharField(max_length=10, choices=Condition.choices) 

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model.brand.name} {self.model.name} ({self.year})"

class VehicleImage(models.Model):
    """  Stores images for a vehicle"""
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="vehicle_images/")

    def __str__(self):
        return f"Image for {self.vehicle.model.brand.name} {self.vehicle.model.name}"

class VehicleFeature(models.Model):
    """  Represents a feature such as Sunroof, Bluetooth"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class VehicleFeaturesMapping(models.Model):
    """  Maps vehicles to their features (Many-to-Many Relationship)"""
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="vehicle_features")
    feature = models.ForeignKey(VehicleFeature, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("vehicle", "feature")

    def __str__(self):
        return f"{self.vehicle.model.brand.name} {self.vehicle.model.name} - {self.feature.name}"
