from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    LAN_ORIGIN_CHOICES = [
        ("NL", "Dutch"),
        ("EN", "English"),
        ("CN", "Chinese"),
    ]
    image = models.ImageField("image of the card", upload_to="card", default='')
    lan = models.CharField("language", max_length=2, choices=LAN_ORIGIN_CHOICES, default='')
    text = models.CharField("text extration of the image", max_length=500, default='', blank=True)
    creation_date = models.DateTimeField("date created")
    modification_date = models.DateTimeField("date modified", blank=True)
    upload_by_userName = models.CharField(max_length=30, default='')
    def __str__(self):
        return self.image.name

class CardAnswer(models.Model):
    CARD_ANSWER_CHOICES = [
        ("FL", "flash"),
        ("DN", "done"),
        ("PA", "pass"),
        ("RE", "repeat")
    ]
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=2, choices=CARD_ANSWER_CHOICES)

class UserCardAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    answer = models.ForeignKey(CardAnswer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

