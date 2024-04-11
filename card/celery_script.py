from celery import shared_task
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.apps import apps

@shared_task
def convert_img_png(card_id):
    Card = apps.get_model('card', 'Card')
    card = Card.objects.get(id=card_id)
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
        card.save()  # Save model with new PNG image