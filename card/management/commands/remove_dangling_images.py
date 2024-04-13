from django.core.management.base import BaseCommand
from card.models import Card
import os
from django.conf import settings


class Command(BaseCommand): 
    help = 'Remove dangling images that are not in the record of db.'

    def handle(self, *args, **options):

        media_dir = settings.MEDIA_ROOT
        card_dir = os.path.join(media_dir, 'card')
        png_dir = os.path.join(media_dir, 'png')

        # Get all original_image and png_image filenames
        original_image_names = set(Card.objects.exclude(original_image='').values_list('original_image', flat=True))
        png_image_names = set(Card.objects.exclude(png_image='').values_list('png_image', flat=True))

        # Remove directory path from filenames
        original_image_names = {os.path.basename(name) for name in original_image_names}
        png_image_names = {os.path.basename(name) for name in png_image_names}

        # Delete images in card directory that do not belong to any Card object
        for filename in os.listdir(card_dir):
            file_path = os.path.join(card_dir, filename)
            if os.path.isfile(file_path) and filename not in original_image_names:
                os.remove(os.path.join(card_dir, filename))
                print(f'Removed {filename} from card directory')

        for filename in os.listdir(png_dir):
            file_path = os.path.join(png_dir, filename)
            if os.path.isfile(file_path) and filename not in png_image_names:
                os.remove(file_path)
                print(f'Removed {filename} from png directory')