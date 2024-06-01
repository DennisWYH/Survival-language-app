from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import Http404
from .models import Card, UserCardAnswer
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from user.models import UserProfile
from translator.models import TextTranslator, TextTokenizer
from django.shortcuts import render
import random

class UserCardAnswerForm(forms.Form):
    CARD_ANSWER_CHOICES = [
        ("FL", "FLASH"),
        ("DN", "DONE"),
        ("PA", "PASS"),
    ]
    answer = forms.ChoiceField(choices=CARD_ANSWER_CHOICES, widget=forms.RadioSelect)

def index(request, language='nl'):
    if request.user.is_authenticated:
        language = UserProfile.objects.get(user=request.user).target_lan

    cards = Card.objects.filter(lan=language)
    if request.user.is_authenticated:
        user_card_answers = UserCardAnswer.objects.filter(user=request.user)
        user_answers = {uca.card.id: uca.answer for uca in user_card_answers}

        # Add the user's answer to each card
        for card in cards:
            card.user_answer = user_answers.get(card.id)

    else:
        for card in cards:
            card.user_answer = None

    paginator = Paginator(cards, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    limit = paginator.per_page
    offset = 0
    if page_number is not None:
        offset = (int(page_number) -1) * limit
    safeOffset, safeLimit = safeOffsetLimit(len(cards), offset, limit)
    cards = cards[safeOffset:safeOffset+safeLimit]

    template = loader.get_template("card/card_index.html")
    context = {
        "cards": cards,
        "language": language,
        "page_obj": page_obj,
    }
    return HttpResponse(template.render(context, request))


def safeOffsetLimit(total, offset, limit):
    if total == 0:
        return 0, 0
    if offset < 0:
        offset = 0
        if limit > total:
            limit = total-1
    elif offset < total-limit:
        return offset, limit
    elif offset >= total - limit and offset <= total:
        limit = total-1
        return offset, limit
    else:
        offset = total
        limit = 0
        return offset, limit

@csrf_exempt
def detail(request, card_id, language=None):
    if request.method == 'GET':
        try:
            card = Card.objects.get(pk=card_id)
            translator = TextTranslator.objects.get(card=card)
            tokenizer = TextTokenizer.objects.get(card=card)
        except Card.DoesNotExist:
            raise Http404("Card does not exist")

        form = UserCardAnswerForm()
        user_card_answer = None
        if request.user.is_authenticated:
            try:
                user_card_answer = UserCardAnswer.objects.get(user=request.user, card=card)
            except UserCardAnswer.DoesNotExist:
                pass

        if language:
            previous_card = Card.objects.filter(pk__lt=card_id, lan=language).order_by('-id').first()
            next_card = Card.objects.filter(pk__gt=card_id, lan=language).order_by('id').first()
        else:
            previous_card = Card.objects.filter(pk__lt=card_id).order_by('-id').first()
            next_card = Card.objects.filter(pk__gt=card_id).order_by('id').first()

        template = loader.get_template("card/card_detail.html")
        context = {
            "card": card,
            'form': form,
            'user_card_answer': user_card_answer,
            'previous_card': previous_card,
            'next_card': next_card,
            'tokens': tokenizer.tokens,
            'tokens_translated': translator.tokens_translated,
        }
        return HttpResponse(template.render(context, request))

def game(request, language=None):
    if request.method == 'GET':
        cards = Card.objects.filter(lan=language)
        two_cards = random.sample(list(cards), 2)

        template = loader.get_template("card/card_game.html")
        context = {
            'two_cards': two_cards,
        }
        return HttpResponse(template.render(context, request))

@login_required
def update_answer(request, card_id):
    if request.method == 'POST':
        answer = request.POST.get('answer')
        card = Card.objects.get(pk=card_id)
        user_card_answer, created = UserCardAnswer.objects.update_or_create(
            user=request.user, card=card, defaults={'answer': answer}
        )
        return JsonResponse({'status': 'success'})
    
# A customer server error view
def server_error(request):
    return render(request, "card/500.html")