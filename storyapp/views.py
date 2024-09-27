from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User,Group
import google.generativeai as palm
palm.configure(api_key='AIzaSyAT1VQThfonpDb9Rexw__6aipCcrgcrxv0')

def index(request):
    #model = palm.GenerativeModel('gemini-pro')

    #prompt = "Create one story for kids of 5 years age on the genre adventure. Each time create an unique story"
    #response = model.generate_content(prompt)

#    response.text 

    user = request.user 
    if user.is_authenticated:
        uname = User.objects.get(username=user)    

        return render(request, 'index.html', {"uname":uname})

    return render(request, 'index.html')


def profile(request):
    user = request.user 
    if user.is_authenticated:
        uname = User.objects.get(username=user)
        try:
            return render(request, 'profile.html', {"uname":uname})
        except user.DoesNotExist:
            return redirect('/login_view')
    else:
        return redirect('/login_view')
    

def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/profile')
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/profile')
        else:
            message = 'Invalid username or password. Please try again.'
            return render(request, 'login.html', {"message": message})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/login_view')