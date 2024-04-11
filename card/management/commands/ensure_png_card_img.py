from django.core.management.base import BaseCommand
from card.models import Card

from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO


class Command(BaseCommand):
    help = 'Generate PNG image for card objects if they dont have it yet.'

    def add_arguments(self, parser):
        parser.add_argument('--card_id', type=int)

    def handle(self, *args, **options):
        print("--- command handler called ----")

        card_id = options.get('card_id')
        if card_id:
            cards = Card.objects.filter(id=card_id)
        else:
            cards = Card.objects.all()
        for card in cards:
            if card.original_image and card.original_image.name.lower().endswith('.png'):
                card.png_image.save(card.original_image.name, card.original_image, save=False)
                card.png_image_exist = True
                card.save()
                print(f"PNG image is already PNG , {card.id}, {card.original_image.name}")
                continue

            if card.original_image is None:
                print(f"Card has no image field, {card.id}, deleting...")
                card.delete()
                continue
            
            if card.png_image_exist:
                print(f"Card already has PNG, {card.id}")
                continue

            if card.original_image:
                # Open the original image using Pillow
                img = Image.open(card.original_image)

                # Convert the image to PNG
                output = BytesIO()
                img.save(output, format='PNG')
                output.seek(0)

                content_file = ContentFile(output.read())
                file_name = f"{card.original_image.name.split('.')[0]}.png"

                # Save the new PNG image
                card.png_image.save(file_name, content_file, save=False)
                card.png_image_exist = True
                card.save()  # Save model with new PNG image
                print(f"Making PNG image for card, {card.id}, {card.original_image.name}")

