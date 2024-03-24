from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import Http404
from .models import Card, UserCardAnswer
from django import forms
from django.views.decorators.csrf import csrf_exempt

class UserCardAnswerForm(forms.Form):
    CARD_ANSWER_CHOICES = [
        ("FL", "FLASH"),
        ("DN", "DONE"),
        ("PA", "PASS"),
        ("RE", "REPEATE")
    ]
    answer = forms.ChoiceField(choices=CARD_ANSWER_CHOICES, widget=forms.RadioSelect)

@login_required
def index(request):
    cards = Card.objects.all()
    user_card_answers = UserCardAnswer.objects.filter(user=request.user)

    user_answers = {uca.card.id: uca.answer.answer_text for uca in user_card_answers}

    # Add the user's answer to each card
    for card in cards:
        card.user_answer = user_answers.get(card.id)


    template = loader.get_template("card/card_index.html")
    context = {
        "cards": cards,
    }
    return HttpResponse(template.render(context, request))

def detail(request, card_id):
    if request.method == 'GET':
        try:
            card = Card.objects.get(pk=card_id)
        except Card.DoesNotExist:
            raise Http404("Card does not exist")

        form = UserCardAnswerForm()

        template = loader.get_template("card/card_detail.html")
        context = {
            "card": card,
            'form': form,
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
def update_answer(request, card_id):
    if request.method == 'POST':
        user = request.user
        answer_text = request.POST.get('answer')
        card_answer = CardAnswer.objects.get(answer_text=answer_text)
        
        UserCardAnswer.objects.update_or_create(
            user=user, 
            card_id=card_id, 
            defaults={'answer': card_answer}
        )

        return JsonResponse({'status': 'success'})