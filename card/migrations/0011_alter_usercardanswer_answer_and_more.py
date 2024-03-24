# Generated by Django 4.2.11 on 2024-03-24 11:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('card', '0010_card_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercardanswer',
            name='answer',
            field=models.CharField(choices=[('FL', 'flash'), ('DN', 'done'), ('PA', 'pass'), ('RE', 'repeat')], max_length=2),
        ),
        migrations.AlterUniqueTogether(
            name='usercardanswer',
            unique_together={('user', 'card')},
        ),
        migrations.DeleteModel(
            name='CardAnswer',
        ),
    ]
