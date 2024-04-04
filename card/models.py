from django.db import models
from django.contrib.auth.models import User
from nltk.tokenize import word_tokenize
from translator.models import TextTranslator
from deep_translator import GoogleTranslator, NotValidPayload, NotValidLanguage

class Card(models.Model):
    LAN_ORIGIN_CHOICES = [
        ("nl", "Dutch"),
        ("en", "English"),
        ("cn", "Chinese"),
        ("it", "Italian"),
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
    comment = models.CharField("comment", max_length=500, default='', blank=True)
    image = models.ImageField("image of the card", upload_to="card", default='')
    lan = models.CharField("language", max_length=2, choices=LAN_ORIGIN_CHOICES, default='')
    grade = models.CharField("grade", max_length=3, choices=GRADE_CHOICES, default='')
    text = models.CharField("text extration of the image", max_length=500, default='', blank=True)
    creation_date = models.DateTimeField("date created")
    modification_date = models.DateTimeField("date modified", blank=True)
    upload_by_userName = models.CharField(max_length=30, default='')
    def __str__(self):
        return self.image.name
    
    def get_language_code(lan_name):
        LAN_ORIGIN_CHOICES = [
            ("nl", "Dutch"),
            ("en", "English"),
            ("cn", "Chinese"),
            ("it", "Italian"),
        ]
        for code, name in LAN_ORIGIN_CHOICES:
            if name.lower() == lan_name.lower():
                return code
        return None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        tokens = word_tokenize(self.text)
        try:
            enTrans = GoogleTranslator(source='nl', target='en').translate(self.text)
            translator = TextTranslator(card=self, translated_text=enTrans, tokens=tokens)
            translator.save()
        except (NotValidPayload, NotValidLanguage) as e:
            print(f"Translation error: {e}")
            pass
class UserCardAnswer(models.Model):
    CARD_ANSWER_CHOICES = [
        ("FL", "flash"),
        ("DN", "done"),
        ("PA", "pass"),
        ("RE", "repeat")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    answer = models.CharField(max_length=2, choices=CARD_ANSWER_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user.username}\nCard ID: {self.card.id}\nAnswer: {self.get_answer_display()}\nTimestamp: {self.timestamp}\n"
    class Meta:
        unique_together = ('user', 'card',)

class UserScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateField()    
