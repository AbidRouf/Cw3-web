from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse
from datetime import datetime

def login_view(request: HttpRequest) -> HttpResponse:
    """
    Handles use login. and authenticates credentials before redirecting to 'home' on success or returning an error message
    on potential failiure 
    """
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
    """This handle the user registration, then validates input befre creating a new user then redirecting the user to 'login' on success or will display a corresponding error depended on failiure """
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
        dob=user_dob
    )
    user.save()
    messages.success(request, "You have successfully registered")
    return redirect('login')
    


def auth_status(request):
    if request.user.is_authenticated:
        hobbies = list(request.user.hobbies.values_list('name', flat=True))
        user_data = {
            'isAuthenticated': True,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'dob': request.user.dob,  # Date of Birth
                'hobbies': hobbies,
            }
        }
    else:
        user_data = {
            'isAuthenticated': False,
            'user': None
        }
    return JsonResponse(user_data)

    



def main_spa(request: HttpRequest) -> HttpResponse:
    """
    This function renders the SPA main page.
    """
    return render(request, 'api/spa/index.html', {})

def logout_view(request: HttpRequest) -> JsonResponse:
    """
    handles the user logout. the request is a POST request, logs out the user and
    returns a success message. Otherwise, returns an error message.
    """
    if request.method == "POST":
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
