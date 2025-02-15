from django.db import models
from django.contrib.auth import get_user_model
from marketplace.models.vehicle import Vehicle

User = get_user_model()

class Chat(models.Model):
    """  Represents a chat between a buyer and a seller"""
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer_chats")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller_chats")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="chats")
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    """  Represents a message in a chat"""
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
