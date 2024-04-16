# Generated by Django 5.0.3 on 2024-04-16 16:56

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('card', '0023_alter_card_png_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordGradeByScience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algorism_name', models.CharField(choices=[('simple_magic', 'The first simple algorism')], default='', max_length=50)),
                ('average_grade_number', models.FloatField(default='', max_length=10)),
                ('token_grade_list', models.JSONField(default=dict)),
                ('creation_date', models.DateTimeField(blank=True, default=datetime.datetime(2024, 4, 16, 18, 56, 4, 634534), verbose_name='date created')),
                ('modification_date', models.DateTimeField(blank=True, default=datetime.datetime(2024, 4, 16, 18, 56, 4, 634534), verbose_name='date modified')),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ranking', to='card.card')),
            ],
        ),
    ]
