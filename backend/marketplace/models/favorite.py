from django.db import models
from django.contrib.auth import get_user_model
from marketplace.models.vehicle import Vehicle

User = get_user_model()

class Favorite(models.Model):
    """  Stores favorite vehicles for a user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "vehicle")

    def __str__(self):
        return f"{self.user.username} favorited {self.vehicle.model.brand.name} {self.vehicle.model.name}"
