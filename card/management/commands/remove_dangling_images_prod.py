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
        print("---- collection of original image db names", original_image_names)

        # Remove directory path from filenames
        original_image_names = {os.path.basename(name) for name in original_image_names}
        png_image_names = {os.path.basename(name) for name in png_image_names}

        # Create a resource using your AWS credentials
        s3 = boto3.resource('s3',endpoint_url="https://ams3.digitaloceanspaces.com",aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        s3Client = boto3.client('s3',aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),endpoint_url=os.getenv('AWS_S3_ENDPOINT_URL'))

        # Specify your bucket name
        bucket_name = "languagereference"
        bucket = s3.Bucket(bucket_name)
        all_files = bucket.objects.all()

        # Delete images in card directory that do not belong to any Card object
        for file in all_files:
            filename = os.path.basename(file.key)
            print("bucket file name", filename)
            if filename not in original_image_names:
                print("bucket file name not in db", filename, "removing")
                s3Client.delete_object(Bucket="media", Key=file.key)

        # This works to delete one object
        # s3Client = boto3.client('s3',aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),endpoint_url=os.getenv('AWS_S3_ENDPOINT_URL'))
        # result = s3Client.delete_object(Bucket="media", Key="card/caterpillar.png")


        # To have the correct access you need to remove the bucket name from the endpoint url
        # s3Resource = boto3.resource('s3', endpoint_url="https://ams3.digitaloceanspaces.com", aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        # bucket = s3Resource.Bucket('languagereference')