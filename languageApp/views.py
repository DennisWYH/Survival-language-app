from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("User logged in")
        else:
            return HttpResponse("Invalid username or password")
    else:
        # Render the login form
        return render(request, 'site_login.html')