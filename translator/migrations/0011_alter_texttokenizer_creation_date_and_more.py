# Generated by Django 5.0.3 on 2024-04-09 18:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translator', '0010_remove_texttranslator_tokens_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='texttokenizer',
            name='creation_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 4, 9, 20, 33, 3, 683137), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='texttokenizer',
            name='modification_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 4, 9, 20, 33, 3, 683137), verbose_name='date modified'),
        ),
        migrations.AlterField(
            model_name='texttranslator',
            name='creation_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 4, 9, 20, 33, 3, 682430), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='texttranslator',
            name='modification_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 4, 9, 20, 33, 3, 682430), verbose_name='date modified'),
        ),
    ]
