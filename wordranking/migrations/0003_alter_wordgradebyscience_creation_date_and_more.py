# Generated by Django 5.0.3 on 2024-04-16 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordranking', '0002_alter_wordgradebyscience_average_grade_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordgradebyscience',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='wordgradebyscience',
            name='modification_date',
            field=models.DateTimeField(auto_now=True, verbose_name='date modified'),
        ),
    ]