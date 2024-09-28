from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages


from .models import Account,History

import google.generativeai as palm
palm.configure(api_key='AIzaSyAT1VQThfonpDb9Rexw__6aipCcrgcrxv0')



def index(request):
    user = request.user 
    if user.is_authenticated:
        uname = User.objects.get(username=user)    
        return render(request, 'index.html', {"uname":uname})

    return render(request, 'index.html')

def engine(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')
        age_group = 10
        user = request.user 
        if user.is_authenticated:
            uname = User.objects.get(username=user)
            # Fetch age from the Account model
            account = Account.objects.get(reg=user)
            age_group = account.age        
        # Generate the story (Assuming you're using an AI model for this part)
        prompt = f"Create a story for kids aged {age_group} on the genre/topic {choice} for more than 500 words. Each time create a unique story."
        
        model = palm.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        story = response.text
        
        user = request.user
        if user.is_authenticated:
            uname = User.objects.get(username=user)
            return render(request, 'engine.html', {"uname": uname, "story": story})
        
        return render(request, 'engine.html', {"story": story})

    return render(request, 'engine.html')


def profile(request):
    user = request.user  # Get the logged-in user

    # Check if the user is authenticated
    if user.is_authenticated:
        # Fetch the associated Account object
        try:
            account = Account.objects.get(reg=user)  # 'reg' is the ForeignKey to User
            # Render the profile template with the account details
            return render(request, 'profile.html', {"account": account})
        except Account.DoesNotExist:
            return redirect('/login_view')  # Redirect if the account doesn't exist
    else:
        return redirect('/login_view')  # Redirect to login if the user is not authenticated


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
            messages.error(request, '*user doesnot exists! try creating one')
            return redirect('/login_view')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/login_view')

def register(request):
    user = request.user 
    if user.is_authenticated:
        return redirect('/profile')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            contact_no = request.POST['contact_no']
            email = request.POST['email']
            age = request.POST['age']

            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, '*username already exists! try another username')
                return redirect('/register')

            # Create a new user in the default User model
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()

            # Create an entry in the custom Account model
            account = Account.objects.create(
                reg=user,
                contact_no=contact_no,
                email=email,
                age=age
            )
            account.save()

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/profile')

        return render(request, 'register.html')
    
def history(request):
    user = request.user 
    if user.is_authenticated:
        uname = User.objects.get(username=user)    
        return render(request, 'history.html', {"uname":uname})
    
    return render(request, 'history.html')