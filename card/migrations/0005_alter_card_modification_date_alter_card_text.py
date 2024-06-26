# Generated by Django 5.0.3 on 2024-03-09 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0004_card_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='modification_date',
            field=models.DateTimeField(blank=True, verbose_name='date modified'),
        ),
        migrations.AlterField(
            model_name='card',
            name='text',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='text'),
        ),
    ]
