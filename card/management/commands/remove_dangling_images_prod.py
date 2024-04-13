import os
import boto3
from card.models import Card
from django.core.management.base import BaseCommand

class Command(BaseCommand): 
    help = 'Remove dangling images that are not in the record of db.'

    def handle(self, *args, **options):

        # Get all original_image and png_image filenames
        original_image_names = set(Card.objects.exclude(original_image='').values_list('original_image', flat=True))
        png_image_names = set(Card.objects.exclude(png_image='').values_list('png_image', flat=True))

        # Remove directory path from filenames
        original_image_names = {os.path.basename(name) for name in original_image_names}
        png_image_names = {os.path.basename(name) for name in png_image_names}

        # Create a session using your AWS credentials
        s3 = boto3.resource('s3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        endpoint_url=os.getenv('AWS_S3_ENDPOINT_URL'))

        # Specify your bucket name
        bucket_name = "languagereference"

        response = s3.list_objects_v2(Bucket=bucket_name)

        if 'Contents' in response:
            all_files = response['Contents']

            # Delete images in card directory that do not belong to any Card object
            for file in all_files:
                filename = os.path.basename(file['Key'])
                if filename not in original_image_names and 'card' in file['Key']:
                    s3.delete_object(Bucket=bucket_name, Key=file['Key'])
                    print(f'Removed {filename} from card directory')

            # Delete images in png directory that do not belong to any Card object
            for file in all_files:
                filename = os.path.basename(file['Key'])
                if filename not in png_image_names and 'png' in file['Key']:
                    s3.delete_object(Bucket=bucket_name, Key=file['Key'])
                    print(f'Removed {filename} from png directory')