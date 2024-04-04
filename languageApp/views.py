from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from user.models import UserProfile
from card.models import UserCardAnswer
from datetime import datetime, timedelta

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            user = User.objects.get(email=username)
            if user.check_password(password):
                login(request, user)
                return redirect('/')
        elif user is not None:
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse("Invalid username or password", status=401)
    else:
        # Render the login form
        return render(request, 'site_login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
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

                 userProfile = UserProfile.objects.create(user=user, email=email, target_lan='nl', grade=4, night_mode=False)
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

def calculateCurrentScore(user):
    # TODO: Need to calculatethe score based on the language selection
    two_months_ago = datetime.now() - timedelta(days=60)
    answers = UserCardAnswer.objects.filter(user=user, timestamp__gte=two_months_ago)
    scores = sorted([grade_to_score(answer.card.grade) for answer in answers], reverse=True)[:10]
    averageScore = sum(scores)/len(scores) if scores else 0
    return averageScore

def progress_view(request):
    if request.user.is_authenticated:
        score = calculateCurrentScore(request.user)
    else: score = 0
    return render(request, 'site_progress.html', {'score': score})

def grade_to_score(grade):
    mapping = {
        "4": 400,
        "5": 500,
        "6a": 600,
        "6a+": 625,
        "6b": 650,
        "6b+": 675,
        "6c": 700,
        "6c+": 725,
        "7a": 750,
        "7a+": 775,
        "8": 800,
    }
    return mapping.get(grade, 0)
