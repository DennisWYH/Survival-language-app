# Generated by Django 5.0.3 on 2024-04-10 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0018_remove_card_image_card_original_image_card_png_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='png_image',
            field=models.ImageField(blank=True, default='', upload_to='card', verbose_name='png version of the image'),
        ),
    ]
