from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Card
from django.template import loader
from django.http import Http404
from .models import Card, UserCardAnswer

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
    try:
        card = Card.objects.get(pk=card_id)
    except Card.DoesNotExist:
        raise Http404("Card does not exist")
    template = loader.get_template("card/card_detail.html")
    context = {
        "card": card,
    }
    return HttpResponse(template.render(context, request))