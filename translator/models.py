from datetime import datetime

from django.db import models
from django.db.models import JSONField
from nltk.tokenize import word_tokenize
from deep_translator import GoogleTranslator

from card.models import Card

class TextTranslator(models.Model):
    """Model for translating text on a card."""
    card = models.OneToOneField(
        Card, on_delete=models.CASCADE, related_name="translations"
    )
    translated_text = models.CharField(max_length=1000, default="", blank=True)
    tokens_translated = JSONField(default=list, blank=True)

    # Some basic date fields
    creation_date = models.DateTimeField("date created", blank=True)
    modification_date = models.DateTimeField("date modified", blank=True)

    def make_translations(self, source_lan):
        """Translate the text on the card."""
        target_lan = "en"
        if not self.translated_text:
            try:
                enTrans = GoogleTranslator(
                    source=source_lan, target=target_lan
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
                        source=source_lan, target=target_lan
                    ).translate(token)
                    self.tokens_translated.append(translated_token)
                except Exception as e:
                    print(f"Translation error: {e}")    

    def __str__(self):
        return self.card.image.name

    def save(self, *args, **kwargs):
        source_lan = self.card.lan
        if source_lan == "nl" or source_lan == "fr" or source_lan == "it":
            self.make_translations(source_lan)
        super().save(*args, **kwargs)

class TextTokenizer(models.Model):
    """Model for tokenizing text on a card."""
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
    
    def make_tokens(self):
        """Tokenize the text on the card."""
        if not self.tokens:
            self.tokens = word_tokenize(self.card.text)
    def save(self, *args, **kwargs):
        if not self.tokens:
            self.make_tokens()
        super().save(*args, **kwargs)
