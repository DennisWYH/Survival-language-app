from django.http import HttpResponse
from .models import Card
from django.template import loader
from django.http import Http404

def index(request):
    allCards = Card.objects.all()
    template = loader.get_template("card/card_index.html")
    context = {
        "cards": allCards,
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