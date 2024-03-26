from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import Http404
from .models import Card, UserCardAnswer
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

class UserCardAnswerForm(forms.Form):
    CARD_ANSWER_CHOICES = [
        ("FL", "FLASH"),
        ("DN", "DONE"),
        ("PA", "PASS"),
        ("RE", "REPEATE")
    ]
    answer = forms.ChoiceField(choices=CARD_ANSWER_CHOICES, widget=forms.RadioSelect)

@login_required
def index(request, language=None):
    if language:
        cards = Card.objects.filter(lan=language)
    else:
        cards = Card.objects.all()
    user_card_answers = UserCardAnswer.objects.filter(user=request.user)

    user_answers = {uca.card.id: uca.answer for uca in user_card_answers}

    # Add the user's answer to each card
    for card in cards:
        card.user_answer = user_answers.get(card.id)


    template = loader.get_template("card/card_index.html")
    context = {
        "cards": cards,
        "language": language,
    }
    return HttpResponse(template.render(context, request))

def about(request):
    return render(request, "card/card_about.html")

def detail(request, card_id, language=None):
    if request.method == 'GET':
        try:
            card = Card.objects.get(pk=card_id)
        except Card.DoesNotExist:
            raise Http404("Card does not exist")

        form = UserCardAnswerForm()
        try:
            user_card_answer = UserCardAnswer.objects.get(user=request.user, card=card)
        except UserCardAnswer.DoesNotExist:
            user_card_answer = None

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
        }
        return HttpResponse(template.render(context, request))
    
    # if request.method == 'POST':
    #     form = UserCardAnswerForm(request.POST)
    #     if form.is_valid():
    #         UserCardAnswer.objects.update_or_create(
    #             user=request.user,
    #             card=card,
    #             defaults={'answer': form.cleaned_data['answer']}
    #         )
    #         return redirect('card_detail', card_id=card_id)

@csrf_exempt
@login_required
def update_answer(request, card_id):
    if request.method == 'POST':
        user = request.user
        answer = request.POST.get('answer')
        card = Card.objects.get(pk=card_id)
        user_card_answer, created = UserCardAnswer.objects.update_or_create(
            user=request.user, card=card, defaults={'answer': answer}
        )
        
        return JsonResponse({'status': 'success'})