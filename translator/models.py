
from django.db import models
from django.db.models import JSONField
from nltk.tokenize import word_tokenize
from deep_translator import GoogleTranslator
import jieba

from django.apps import apps

class TextTranslator(models.Model):
    """Model for translating text on a card."""
    card = models.OneToOneField(
        'card.Card', on_delete=models.CASCADE, related_name="translations"
    )
    translated_text = models.CharField(max_length=1000, default="", blank=True)
    tokens_translated = JSONField(default=list, blank=True)

    # Some basic date fields
    creation_date = models.DateTimeField("date created", auto_now_add=True, blank=True)
    modification_date = models.DateTimeField("date modified",auto_now=True, blank=True)

    def ensure_translations(self, source_lan):
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
                 # Get the TextTokenizer model
                Tokenizer = apps.get_model('translator', 'TextTokenizer')
                tokenizer = Tokenizer.objects.get(card=self.card)
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
        return self.card.original_image.name

    def save(self, *args, **kwargs):
        source_lan = self.card.lan
        match source_lan:
            case "cn":
                self.ensure_translations("zh-CN")
            case _:
                self.ensure_translations(source_lan)
        super().save(*args, **kwargs)

class TextTokenizer(models.Model):
    """Model for tokenizing text on a card."""
    card = models.OneToOneField(
        'card.Card', on_delete=models.CASCADE, related_name="tokens"
    )
    tokens = JSONField(default=list, blank=True)

    # Some regular date fields
    creation_date = models.DateTimeField("date created", auto_now_add=True, blank=True)
    modification_date = models.DateTimeField("date modified", auto_now=True, blank=True)

    def __str__(self):
        return self.card.original_image.name
    
    # nltk doesn't support chinese tokenization
    def nltk_make_tokens(self):
        """Tokenize the text on the card."""
        self.tokens = word_tokenize(self.card.text, language=self.card.get_language_display())

    # we use jieba to tokenize mandarin
    def jieba_make_tokens(self):
        """Tokenize the text on the card."""
        seg_list = jieba.cut(self.card.text, cut_all=False)
        self.tokens = list(seg_list)

    def save(self, *args, **kwargs):
        # On creating textTokenizer object, we try to create tokens field for the object if it doesn't exist yet
        if not self.tokens:
            if self.card.lan == "cn":
                self.jieba_make_tokens()
            else:
                self.nltk_make_tokens()
        super().save(*args, **kwargs)
