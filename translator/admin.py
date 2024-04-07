from django.contrib import admin
from .models import TextTranslator


class TextTranslatorAdmin(admin.ModelAdmin):
    fields = ["card", "translated_text", "tokens", "tokens_translated"]
    list_display = ["card", "card_modification_date", "translated_text", "tokens", "tokens_translated"]

    def card_modification_date(self, obj):
        return obj.card.modification_date
    card_modification_date.short_description = 'Card Modification Date'

admin.site.register(TextTranslator, TextTranslatorAdmin)
