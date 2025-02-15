from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    """  Stores notifications for users about messages, sales, price changes, etc."""
    
    class NotificationType(models.TextChoices):
        MESSAGE = "Message"
        VEHICLE_SOLD = "Vehicle Sold"
        PRICE_DROP = "Price Drop"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )  #   Links notification to a user

    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  #   Indexed for sorting

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),  #   Faster sorting by date
            models.Index(fields=["is_read"]),  #   Optimize unread notification queries
        ]
