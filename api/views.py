from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from datetime import datetime

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect('home')  
        else:
            messages.error(request, "Invalid credentials.")
            return render(request, 'api/login.html', {'error': 'Invalid credentials.'})
    else:  
        return render(request, 'api/login.html')

def signup_view(request):
    if request.method == 'GET':
        return render(request, 'api/signup.html')
    
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']
    dob = request.POST['dob']

    if password != password2:
        messages.error(request, "Password don't match")
        return redirect('signup')
    
    User = get_user_model()

    if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return redirect('signup')
    
    if User.objects.filter(email=email).exists():
        messages.error(request, 'That email is taken')
        return redirect('signup')
    
    if not dob:
        messages.error(request, "Please enter date of birth")
        return redirect('signup')
    
    try:
        user_dob = datetime.strptime(dob, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, "Invalid dob")

    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        dob=dob
    )
    user.save()
    messages.success(request, "You have successfully registered")
    return redirect('login')
    


    



def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})
