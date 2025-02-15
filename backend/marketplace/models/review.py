from django.db import models
from django.contrib.auth import get_user_model
from marketplace.models.vehicle import Vehicle

User = get_user_model()

class Review(models.Model):
    """✅ Stores reviews for users and vehicles"""
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="written_reviews"
    )
    reviewed_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_reviews"
    )
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="reviews"
    )

    parent_review = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )  # ✅ Enables replies to reviews

    rating = models.IntegerField(db_index=True)  # ✅ Indexed for fast filtering
    review_text = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True, db_index=True)  # ✅ Index for sorting

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewed_user.username} on {self.vehicle.model.brand.name} {self.vehicle.model.name}"

    class Meta:
        indexes = [
            models.Index(fields=["rating"]),  # ✅ Fast filtering by rating
            models.Index(fields=["review_date"]),  # ✅ Faster sorting by date
        ]
