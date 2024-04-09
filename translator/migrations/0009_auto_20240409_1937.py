from django.db import migrations

def migrate_tokens(apps, schema_editor):
    TextTranslator = apps.get_model('translator', 'TextTranslator')
    TextTokenizer = apps.get_model('translator', 'TextTokenizer')

    for translator in TextTranslator.objects.all():
        tokenizer, _ = TextTokenizer.objects.get_or_create(card=translator.card)
        tokenizer.tokens = translator.tokens
        tokenizer.save()

class Migration(migrations.Migration):

    dependencies = [
        ('translator', '0008_alter_texttranslator_creation_date_and_more'), 
    ]

    operations = [
        migrations.RunPython(migrate_tokens),
    ]