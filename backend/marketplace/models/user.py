from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
      Custom User Model
    - Extends Django's AbstractUser.
    - Stores additional user details like phone number and last seen timestamp.
    - Users can be sellers or buyers.
    """
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    last_seen = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField("auth.Group", related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField("auth.Permission", related_name="custom_user_permissions", blank=True)

    def __str__(self):
        return self.username
