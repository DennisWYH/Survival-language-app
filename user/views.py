from django.shortcuts import render
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from deep_translator import GoogleTranslator


@login_required
@csrf_exempt
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'user/user_profile.html', {'user_profile': user_profile})