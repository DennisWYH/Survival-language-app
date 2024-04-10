from django.contrib import admin
from .models import TextTranslator
from .models import TextTokenizer


class TextTranslatorAdmin(admin.ModelAdmin):
    fields = ["card", "translated_text", "tokens_translated"]
    list_display = [
        "card",
        "card_modification_date",
        "translated_text",
        "tokens_translated",
    ]

    def card_modification_date(self, obj):
        return obj.card.modification_date

    card_modification_date.short_description = "Card Modification Date"


class TextTokenizerAdmin(admin.ModelAdmin):
    fields = ["card", "tokens"]
    list_display = ["card", "tokens"]


admin.site.register(TextTranslator, TextTranslatorAdmin)
admin.site.register(TextTokenizer, TextTokenizerAdmin)
