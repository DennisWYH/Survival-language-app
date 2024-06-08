
from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

class Card(models.Model):
    """Model for a card."""
    LAN_ORIGIN_CHOICES = [
        ("nl", "Dutch"),
        ("cn", "Chinese"),
        ("it", "Italian"),
        ("fr", "French")
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
    png_image = models.ImageField("png image", upload_to="png", default="",blank=True)
    png_image_exist = models.BooleanField("png image exist", default=False)
    thumbnail = models.ImageField("thubmnail image", upload_to="thumbnail", default="",blank=True)
    thumbnail_exist = models.BooleanField("thumbnail image exist", default=False)
    lan = models.CharField(
        "language", max_length=2, choices=LAN_ORIGIN_CHOICES, default=""
    )
    grade = models.CharField("grade", max_length=3, choices=GRADE_CHOICES, default="")
    text = models.CharField(
        "text extration of the image", max_length=500, default="", blank=True
    )
    creation_date = models.DateTimeField("date created", auto_now_add=True)
    modification_date = models.DateTimeField("date modified", auto_now=True, blank=True)
    upload_by_userName = models.CharField(max_length=30, default="")

    def __str__(self):
        return self.original_image.name

    # Displays the human readable language of the language choices, e.g. "French" instead of "fr"
    def get_language_display(self):
        """Return the human-readable language display."""
        return dict(self.LAN_ORIGIN_CHOICES).get(self.lan, "")


    def get_language_code(self, lan_name):
        """Return the language code for a given language name."""
        for code, name in self.LAN_ORIGIN_CHOICES:
            if name.lower() == lan_name.lower():
                return code
        return None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # On creating a new card, create a TextTokenizer object for it
        TextTokenizer = apps.get_model('translator', 'TextTokenizer')

        # On creating a new card, create a TextTranslator object for it
        TextTranslator = apps.get_model('translator', 'TextTranslator')
        try:
            TextTokenizer.objects.get(card=self)
        except ObjectDoesNotExist:
            TextTokenizer.objects.create(card=self)

        try:
            TextTranslator.objects.get(card=self)
        except ObjectDoesNotExist:
            TextTranslator.objects.create(card=self)


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
