from celery import shared_task
from .models import TextTokenizer, TextTranslator

@shared_task
def create_text_tokenizer_and_translator(card_id):
    # create a TextTokenizer instance
    text_tokenizer, created = TextTokenizer.objects.get_or_create(card_id=card_id)

    # create a TextTranslator instance
    text_translator, created = TextTranslator.objects.get_or_create(card_id=card_id)