from django.http import HttpResponse
from .models import Card
from django.template import loader

def index(request):
    card = Card.objects.get(1)
    template = loader.get_template("card/index.html")
    context = {
        "card": card,
    }
    return HttpResponse(template.render(context, request))

def detail(request, card_id):
    card = Card.objects.get(pk=card_id)
    template = loader.get_template("card/card_detail.html")
    context = {
        "card": card,
    }
    print(card)
    return HttpResponse(template.render(context, request))