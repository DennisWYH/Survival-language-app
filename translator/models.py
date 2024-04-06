from django.db import models
from django.db.models import JSONField
from card.models import Card
from nltk.tokenize import word_tokenize
from deep_translator import GoogleTranslator


class TextTranslator(models.Model):
    card = models.OneToOneField(
        Card, on_delete=models.CASCADE, related_name="translations"
    )
    translated_text = models.CharField(max_length=1000, default="", blank=True)
    tokens = JSONField(default=list, blank=True)
    tokens_translated = JSONField(default=list, blank=True)

    def __str__(self):
        return self.card.image.name

    def save(self, *args, **kwargs):
        sourceLan = self.card.lan
        defaultTargetLan = "en"
        if not self.tokens:
            self.tokens = word_tokenize(self.card.text)
        if not self.translated_text:
            try:
                enTrans = GoogleTranslator(
                    source=sourceLan, target=defaultTargetLan
                ).translate(self.card.text)
                self.translated_text = enTrans
            except Exception as e:
                print(f"Translation error: {e}")
        if not self.tokens_translated:
            self.tokens_translated = []
            for token in self.tokens:
                try:
                    translated_token = GoogleTranslator(
                        source=sourceLan, target=defaultTargetLan
                    ).translate(token)
                    self.tokens_translated.append(translated_token)
                except Exception as e:
                    print(f"Translation error: {e}")
        super().save(*args, **kwargs)
