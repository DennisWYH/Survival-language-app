# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'your_app_name/user_profile.html', {'user': user})