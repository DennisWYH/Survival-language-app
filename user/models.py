from django.db import models
from django.contrib.auth.models import User
from card.models import Card

class UserProfile(models.Model):
    """Model for user profile."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(default='')
    target_lan = models.CharField(max_length=2, choices=Card.LAN_ORIGIN_CHOICES, default='')
    grade = models.CharField(max_length=3, choices=Card.GRADE_CHOICES, default='4')
    night_mode = models.BooleanField(default=False)
    creation_date = models.DateTimeField("date created", auto_now_add=True, blank=True)

    
    def __str__(self):
        return self.user.username
    
    def get_target_lan_display(self):
        """Return the display value for target_lan."""
        lan_choices = dict(Card.LAN_ORIGIN_CHOICES)
        return lan_choices.get(self.target_lan, '')