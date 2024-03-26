from django.db import models
from django.contrib.auth.models import User
from card.models import Card

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target_lan = models.CharField(max_length=2, choices=Card.LAN_ORIGIN_CHOICES, default='')
    night_mode = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username