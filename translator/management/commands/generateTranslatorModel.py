from django.core.management.base import BaseCommand
from card.models import Card
from translator.models import TextTranslator

class Command(BaseCommand):
    help = 'Creates a TextTranslator object for each Card that does not have one'

    def handle(self, *args, **options):
        for card in Card.objects.all():
            if not hasattr(card, 'translations'):
                TextTranslator.objects.create(card=card)
                self.stdout.write(self.style.SUCCESS(f'Successfully created TextTranslator for card id {card.id}'))