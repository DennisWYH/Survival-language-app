from io import BytesIO

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.apps import apps
from django.dispatch import receiver
from django.core.files.base import ContentFile
from PIL import Image


class Card(models.Model):
    """Model for a card."""
    LAN_ORIGIN_CHOICES = [
        ("nl", "Dutch"),
        ("cn", "Chinese"),
        ("it", "Italian"),
        ("fr", "French")
        # ("en", "English"), # No english support for now, as I'm not sure what shall be the target language for it
    ]
    GRADE_CHOICES = [
        ("8", "rainbow"),
        ("7a+", "mint"),
        ("7a", "White"),
        ("6c+", "purple"),
        ("6c", "red"),
        ("6b+", "DarkBlue"),
        ("6b", "Yellow"),
        ("6a+", "Orange"),
        ("6a", "Black"),
        ("5", "LightBlue"),
        ("4", "Green"),
    ]
    comment = models.CharField("comment", max_length=500, default="", blank=True)
    original_image = models.ImageField("original image", upload_to="card", default="")
    png_image = models.ImageField("png version of the image", upload_to="card", default="",blank=True)
    lan = models.CharField(
        "language", max_length=2, choices=LAN_ORIGIN_CHOICES, default=""
    )
    grade = models.CharField("grade", max_length=3, choices=GRADE_CHOICES, default="")
    text = models.CharField(
        "text extration of the image", max_length=500, default="", blank=True
    )
    creation_date = models.DateTimeField("date created")
    modification_date = models.DateTimeField("date modified", blank=True)
    upload_by_userName = models.CharField(max_length=30, default="")

    def __str__(self):
        return self.original_image.name

    def get_language_code(self, lan_name):
        """Return the language code for a given language name."""
        for code, name in self.LAN_ORIGIN_CHOICES:
            if name.lower() == lan_name.lower():
                return code
        return None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.original_image:
            # Open the original image using Pillow
            img = Image.open(self.original_image.path)

            # Convert the image to PNG
            output = BytesIO()
            img.save(output, format='PNG')
            output.seek(0)

            # Create a new Django file-like object to hold the image
            content_file = ContentFile(output.read())
            file_name = f"{self.original_image.name.split('.')[0]}.png"

            # Save the new PNG image
            self.png_image.save(file_name, content_file, save=False)
        super().save(*args, **kwargs)  # Save model with new PNG image


class UserCardAnswer(models.Model):
    """Model for user's answer to a card."""
    CARD_ANSWER_CHOICES = [
        ("FL", "flash"),
        ("DN", "done"),
        ("PA", "pass"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    answer = models.CharField(max_length=2, choices=CARD_ANSWER_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user.username}\nCard ID: {self.card.id}\nAnswer: {self.get_answer_display()}\nTimestamp: {self.timestamp}\n"

    class Meta:
        """Define unique_together constraint for UserCardAnswer model."""
        unique_together = (
            "user",
            "card",
        )


class UserScore(models.Model):
    """Model for user's score."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateField()


@receiver(post_save, sender=Card)
def create_text_translator(sender, instance, created, **kwargs):
    """Create a TextTranslator object for a card if the card is created and its language is Dutch or French."""
    if created and (instance.lan == "nl" or instance.lan == "fr"):
        text_translator = apps.get_model("translator", "TextTranslator")
        text_translator.objects.create(card=instance)
