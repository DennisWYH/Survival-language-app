from django.http import HttpResponse
from .models import Card
from django.template import loader

def index(request):
    allCards = Card.objects.all()
    template = loader.get_template("card/card_index.html")
    context = {
        "cards": allCards,
    }
    return HttpResponse(template.render(context, request))

def detail(request, card_id):
    card = Card.objects.get(pk=card_id)
    template = loader.get_template("card/card_detail.html")
    context = {
        "card": card,
    }
    return HttpResponse(template.render(context, request))