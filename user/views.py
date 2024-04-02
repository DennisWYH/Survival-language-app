from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
from card.models import Card
from django.http import JsonResponse
from django.shortcuts import render, redirect

@login_required
@csrf_exempt
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    lan_choices = Card.LAN_ORIGIN_CHOICES
    return render(request, 'user/user_profile.html', {'user_profile': user_profile, 'lan_choices': lan_choices})

@login_required
@csrf_exempt
def update(request):
    if request.method == 'POST':
        target_lan = request.POST.get('target_lan')
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.target_lan = target_lan
        user_profile.save()
        return JsonResponse({'status': 'ok'})

    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'user/user_profile.html', {'user_profile': user_profile})