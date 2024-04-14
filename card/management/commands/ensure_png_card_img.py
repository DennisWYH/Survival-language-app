from django.core.management.base import BaseCommand
from card.models import Card

from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO

import os


class Command(BaseCommand): 
    help = 'Generate PNG image for card objects if they dont have it yet.'

    def add_arguments(self, parser):
        parser.add_argument('--card_id', type=int)

    def png_name_from_original_img(self, card):
        png_img_name = os.path.basename(card.original_image.name)
        png_img_name = f"{png_img_name.split('.')[0]}.png"
        return png_img_name


    def handle(self, *args, **options):
        print("--- ensure_png_card_img command handler called ----")

        card_id = options.get('card_id')
        if card_id:
            cards = Card.objects.filter(id=card_id)
        else:
            cards = Card.objects.all()
        for card in cards:
            if card.original_image and card.original_image.name.lower().endswith('.png'):
                png_img_name = self.png_name_from_original_img(card)
                card.png_image.save(png_img_name, card.original_image, save=False)
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
                # right now the original_image name is as such card/abc.jpg
                # basename would only takes in abc.jpg part
                png_img_name = self.png_name_from_original_img(card)

                # Save the new PNG image
                card.png_image.save(png_img_name, content_file, save=False)
                card.png_image_exist = True
                card.save()  # Save model with new PNG image
                print(f"Making PNG image for card, {card.id}, {card.original_image.name}")

