from django.core.management.base import BaseCommand
from card.models import Card

from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO

import os


class Command(BaseCommand): 
    help = 'Generate PNG image and thumbnail for card objects if they dont have it yet.'

    def add_arguments(self, parser):
        parser.add_argument('--card_id', type=int)

    def png_name_from_original_img(self, card, keep_extension=False):
        png_img_name = os.path.basename(card.original_image.name)
        if not keep_extension:
            name_without_ext = os.path.splitext(png_img_name)
            png_img_name = f"{name_without_ext}.png"
        return png_img_name

    def thumbnail_from_original_img(self, card, keep_extension=False):
        thumbnail_img_name = os.path.basename(card.original_image.name)
        if not keep_extension:
            name_without_ext = os.path.splitext(thumbnail_img_name)
            thumbnail_img_name = f"{name_without_ext[0]}_thumbnail.jpeg"
        return thumbnail_img_name


    def handle(self, *args, **options):
        print("--- ensure_png_card_img command handler called to generatel png and thumbnail ----")

        card_id = options.get('card_id')
        if card_id:
            cards = Card.objects.filter(id=card_id)
        else:
            cards = Card.objects.all()
        for card in cards:
            # Everything in place
            if card.thumbnail_exist and card.png_image_exist:
                print(f"Card already has PNG and thumbnail, {card.id}")
                continue

            # If the card has no image field, nothing to work with
            if card.original_image is None:
                print(f"Card has no image field, {card.id}, deleting...")
                card.delete()
                continue

            # If there is already png, we only need to make thumbnail
            if card.original_image and card.original_image.name.lower().endswith('.png'):
                new_png_name = self.png_name_from_original_img(card, True)
                card.png_image.save(new_png_name, card.original_image, save=False)
                card.png_image_exist = True
                card.save()
                print(f"PNG image is already PNG , {card.id}, {card.original_image.name}")

                img = Image.open(card.original_image)

                output = BytesIO()
                img.thumbnail((128, 128))
                img.save(output, format='PNG')
                output.seek(0)
                content_file = ContentFile(output.read())

                thumbnailName = self.thumbnail_from_original_img(card, False)
                print(f"thumbnail name is, {thumbnailName}")

                card.thumbnail.save(thumbnailName, content_file, save=False)
                card.thumbnail_exist = True
                card.save()
                print(f"Making thumbnail image for card, {card.id}, {card.original_image.name}")
                continue

            # Make both png and thumbnail
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
                png_img_name = self.png_name_from_original_img(card, False)

                # Save the new PNG image
                card.png_image.save(png_img_name, content_file, save=False)
                card.png_image_exist = True
                card.save()  # Save model with new PNG image
                print(f"Making PNG image for card, {card.id}, {card.original_image.name}")

                # Save the new thumgnail image
                img2 = Image.open(card.original_image)

                output2 = BytesIO()
                img2.thumbnail((128, 128))
                img2.save(output2, format='JPEG')
                output2.seek(0)
                content_file2 = ContentFile(output2.read())

                thumbnailName = self.thumbnail_from_original_img(card, False)
                card.thumbnail.save(thumbnailName, content_file2, save=False)
                card.thumbnail_exist = True
                card.save()
                print(f"Making thumbnail image for card, {card.id}, {card.original_image.name}")

