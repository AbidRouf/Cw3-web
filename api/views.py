from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.forms import PasswordChangeForm
from .models import Hobby
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
                'dob': request.user.dob,  
                'hobbies': hobbies,
            }
        }
    else:
        user_data = {
            'isAuthenticated': False,
            'user': None
        }
    return JsonResponse(user_data)


@login_required
@require_http_methods(["GET"])
def profile_view(request):
    try:
        hobbies = list(request.user.hobbies.values_list('name', flat=True))
        user_data = {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'dob': request.user.dob,  
            'hobbies': hobbies,
        }
        return JsonResponse({'success': True, 'user': user_data}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Failed to retrieve profile information.'}, status=500)


@login_required
@require_POST
def change_user_password(request):
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')

    if new_password != confirm_password:
        return JsonResponse({'success': False, 'error': 'Password do not match'}, status=400)

    try:
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return JsonResponse({'success': True, 'message': 'Password updated successfully.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Failed to update password.'}, status=500)

    # form = PasswordChangeForm(user=request.user, data=request.POST)

    # if form.is_valid():
    #     user = form.save()
    #     update_session_auth_hash(request, user)
    #     return JsonResponse({'success': True, 'message': 'Password updated successfully.'}, status=200)
    # else:
    #     errors = form.errors.as_json()
    #     return JsonResponse({'success': False, 'errors': errors}, status=400)

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

def main_spa(request: HttpRequest) -> HttpResponse:
    """
    This function renders the SPA main page.
    """
    return render(request, 'api/spa/index.html', {})
