from django.contrib import admin
from django.contrib.auth.models import User
from .models import Card, UserCardAnswer
from django.utils import timezone
from translator.models import TextTokenizer

class CardAdmin(admin.ModelAdmin):
    fields = [
        "original_image",
        "png_image",
        "text",
        "comment",
        "grade",
        "lan",
        "upload_by_userName",
    ]
    list_display = [
        # "original_image",
        # "png_image",
        "lan",
        "grade",
        "text",
        "upload_by_userName",
    ]
    list_display_links = ["text"]

    def change_view(self, request, object_id, form_url="", extra_context=None):
        # Get the object instance
        obj = Card.objects.get(pk=object_id)
        # Pass the instance to the template context
        extra_context = extra_context or {}
        extra_context["instance"] = obj
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is None:  # Only fill the field for new instances
            form.base_fields["upload_by_userName"].initial = request.user.username
        return form

    def save_model(self, request, obj, form, change):
        if not obj.upload_by_userName:
            obj.upload_by_userName = request.user.username
        super().save_model(request, obj, form, change)
        TextTokenizer.objects.get_or_create(card=obj)


class CardAnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "card", "answer_text"]


class UserCardAnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "card", "answer", "timestamp"]


# Register your models here.
admin.site.register(Card, CardAdmin)
admin.site.register(UserCardAnswer, UserCardAnswerAdmin)
