from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from user.models import UserProfile

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse("Invalid username or password")
    else:
        # Render the login form
        return render(request, 'site_login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            if password == password2:
                 user = User.objects.create_user(username=username, password=password)
                 user.save()

                 userProfile = UserProfile.objects.create(user=user, target_lan='nl', grade=4, night_mode=False)
                 userProfile.save()
            else:
                return HttpResponse("password does not match")
    else:
        return render(request, 'site_signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')

def about_view(request):
    return render(request, 'site_about.html')