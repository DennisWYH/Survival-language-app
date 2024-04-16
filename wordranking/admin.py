from django.contrib import admin
from .models import WordGradeByScience
from translator.models import TextTokenizer

class WordGradeByScienceAdmin(admin.ModelAdmin):
    list_display = ('card', 'get_tokens', 'average_grade_number', 'token_grade_list', 'algorism_name')

    # To add a field of tokens in the admin list view
    def get_tokens(self, obj):
        tokenizer = TextTokenizer.objects.get(card=obj.card)
        return tokenizer.tokens
    get_tokens.short_description = 'Tokens'

admin.site.register(WordGradeByScience, WordGradeByScienceAdmin)