from django.db import models
from django.db.models import JSONField
from card.models import Card
from nltk.tokenize import word_tokenize
from deep_translator import GoogleTranslator
from datetime import datetime

class TextTranslator(models.Model):
    card = models.OneToOneField(
        Card, on_delete=models.CASCADE, related_name="translations"
    )
    translated_text = models.CharField(max_length=1000, default="", blank=True)
    tokens_translated = JSONField(default=list, blank=True)

    # Some basic date fields
    now = datetime.now()
    creation_date = models.DateTimeField("date created", default=now, blank=True)
    modification_date = models.DateTimeField("date modified", default=now, blank=True)

    def makeTranslations(self, sourceLan):
        targetLan = "en"
        if not self.translated_text:
            try:
                enTrans = GoogleTranslator(
                    source=sourceLan, target=targetLan
                ).translate(self.card.text)
                self.translated_text = enTrans
            except Exception as e:
                print(f"Translation error: {e}")
        if not self.tokens_translated:
            try:
                tokenizer = TextTokenizer.objects.get(card=self.card)
            except TextTokenizer.DoesNotExist:
                print("No TextTokenizer associated with this Card.")
                return
            self.tokens_translated = []
            for token in tokenizer.tokens:
                try:
                    translated_token = GoogleTranslator(
                        source=sourceLan, target=targetLan
                    ).translate(token)
                    self.tokens_translated.append(translated_token)
                except Exception as e:
                    print(f"Translation error: {e}")    

    def __str__(self):
        return self.card.image.name

    def save(self, *args, **kwargs):
        sourceLan = self.card.lan
        if sourceLan == "nl" or sourceLan == "fr" or sourceLan == "it":
            self.makeTranslations(sourceLan)
        super().save(*args, **kwargs)

class TextTokenizer(models.Model):
    card = models.OneToOneField(
        Card, on_delete=models.CASCADE, related_name="tokens"
    )
    tokens = JSONField(default=list, blank=True)

    # Some regular date fields
    now = datetime.now()
    creation_date = models.DateTimeField("date created", default=now, blank=True)
    modification_date = models.DateTimeField("date modified", default=now, blank=True)

    def __str__(self):
        return self.card.image.name
    
    def makeTokens(self):
        if not self.tokens:
            self.tokens = word_tokenize(self.card.text)
    def save(self, *args, **kwargs):
        if not self.tokens:
            self.makeTokens()
        super().save(*args, **kwargs)
