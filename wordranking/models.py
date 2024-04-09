from django.db import models
from card.models import Card
from nltk.tokenize import word_tokenize
from deep_translator import GoogleTranslator
from datetime import datetime

# Let's use some statistics to determine the grade of a language text :)
class WordGradeByScience(models.Model):
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

    MAGIC_RECEIPES = [
        ("simple_magic", "The first simple algorism"),
    ]
    card = models.ManyToOneRel(
        Card, on_delete=models.CASCADE, related_name="translations"
    )
    # I might come up with multiple grades for one text according to different algorisms 
    # during experiment period to see which one makes more sense
    algorismName = models.CharField(max_length=50, choices=MAGIC_RECEIPES, default="")
    # Harder words would be given more weights
    overallGrade = models.CharField(max_length=3, choices=GRADE_CHOICES, default="",)

    # Some time fields never do harm
    now = datetime.now()
    creation_date = models.DateTimeField("date created", default=now, blank=True)
    modification_date = models.DateTimeField("date modified", default=now, blank=True)

    def __str__(self):
        return self.card.text

    def save(self, *args, **kwargs):
        sourceLan = self.card.lan
        if sourceLan == "nl" or sourceLan == "fr" or sourceLan == "it":
            self.populateTranslationForDutch(sourceLan)
        super().save(*args, **kwargs)
        