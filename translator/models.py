from django.db import models
from django.contrib.postgres.fields import JSONField
from card.models import Card
from nltk.tokenize import word_tokenize
from deep_translator import GoogleTranslator, NotValidPayload, NotValidLanguage

class TextTranslator(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='translations')
    translated_text = models.CharField(max_length=1000, defaul='')
    tokens = JSONField(default=list)
    tokens_translated = JSONField(default=list)
    def __str__(self):
        return self.translated_text
    def save(self, *args, **kwargs):
        if not self.tokens:
            self.tokens = word_tokenize(self.card.text)
        if not self.translated_text:
            try:
                enTrans = GoogleTranslator(source='nl', target='en').translate(self.text)
                self.translated_text = enTrans 
            except (NotValidPayload, NotValidLanguage) as e:
                print(f"Translation error: {e}")
        if not self.tokens_translated:
                self.tokens_translated = []
                for token in self.tokens:
                    try:
                        translated_token = GoogleTranslator(source='nl', target='en').translate(token)
                        self.tokens_translated.append(translated_token)
                    except (NotValidPayload, NotValidLanguage) as e:
                        print(f"Translation error: {e}")
        super().save(*args, **kwargs)

# Get the card instance
card = Card.objects.get(id=1)

# Tokenize the card.text
tokens = word_tokenize(card.text)

# Create a TextTranslator instance
translator = TextTranslator(card=card, translated_text='', tokens=tokens)
translator.save()