from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, update_session_auth_hash, logout
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.forms import PasswordChangeForm
from .models import Hobby
from collections import Counter
from django.db.models import  Count, Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from datetime import datetime,date , timedelta
import json
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Hobby, FriendRequest  # Assuming FriendRequest is defined in the same models.py file as Hobby

@login_required
def list_friend_requests(request):
    if request.method == "GET":
        # Fetch all pending friend requests to the current user
        friend_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
        
        requests_data = [
            {
                "id": fr.id,
                "from_user_id": fr.from_user.id,
                "from_username": fr.from_user.username,
                "sent_on": fr.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
            for fr in friend_requests
        ]
        
        return JsonResponse({"friend_requests": requests_data}, safe=False, status=200)


@login_required
@require_POST
def send_friend_request(request):
    to_user_id = request.POST.get('to_user_id')
    if not to_user_id:
        return JsonResponse({'success': False, 'error': 'User ID is required.'}, status=400)

    try:
        to_user = User.objects.get(id=to_user_id)
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user, is_active=True).exists():
            return JsonResponse({'success': False, 'error': 'Friend request already sent.'}, status=400)

        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return JsonResponse({'success': True, 'message': 'Friend request sent successfully.'}, status=201)

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

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


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

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
        auth.logout(request)
        return JsonResponse({'message': 'Logged out successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
@require_POST
def create_new_hobby(request):
    """
    This function creates a new hobby and then is used for adding it to the users hobbies,last section will return a successfull or error response
    """
    hobby_name = request.POST.get('hobby')
    if not hobby_name:
        return JsonResponse({'success': False, 'error': 'Hobby name is required.'}, status=400)
    
    try:
        hobby = Hobby.objects.filter(name=hobby_name).first()
        if not hobby:
           hobby = Hobby(name=hobby_name)
           hobby.save()
        request.user.hobbies.add(hobby)
        return JsonResponse({'success': True, 'message': 'Hobby added successfully.'}, status=200)
    except Exception as e:
        print(f"Error adding hobby: {e}")
        return JsonResponse({'success': False, 'error': 'An error  while adding the hobby.'}, status=500)
    
@login_required
@require_POST
def update_profile(request):
    """
    For updating users profile details,then will return a succesfull response if all is added correctly or an error response if not added in intended way
    """
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    dob = request.POST.get('dob')

    try:
        if first_name:
            request.user.first_name = first_name
        if last_name:
            request.user.last_name = last_name
        if email:
            request.user.email = email
        if dob:
            request.user.dob = datetime.strptime(dob, '%Y-%m-%d').date()
        request.user.save()
        return JsonResponse({'success': True, 'message': 'Profile updated successfully.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Failed to update profile.'}, status=500)

def get_all_hobbies(request):
    """
    fetches all hobbies all from the database,and will return a json response as seen on the last line
    """
    hobbies = list(Hobby.objects.values('id', 'name'))
    return JsonResponse({'success': True, 'hobbies': hobbies}, status=200)

def add_hobby(request):
    """
    Adds an existing hobby that is already on the site the other users actual hobbies,then returns a success or error JSON response.
    """
    hobby_id = request.POST.get('hobby_id')
    if hobby_id:
        try:
            hobby = Hobby.objects.get(id=hobby_id)
            request.user.hobbies.add(hobby)
            return JsonResponse({'success': True, 'message': 'Hobby added successfully.'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'Failed to add hobby.'}, status=500)
    else:
        hobby_name = request.POST.get('hobby_name')
        try:
            hobby = Hobby.objects.get(name=hobby_name)
            request.user.hobbies.add(hobby)
            return JsonResponse({'success': True, 'message': 'Hobby added successfully.'}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'Failed to add hobby.'}, status=500)

@login_required
@require_POST
def add_multiple_hobbies(request):
    try:
        data = json.loads(request.body)
        hobby_ids = data.get('hobby_ids', [])
        if not hobby_ids:
            return JsonResponse({'success': False, 'error': 'No hobbies provided.'}, status=400)

        hobbies = Hobby.objects.filter(id__in=hobby_ids)
        if not hobbies.exists():
            return JsonResponse({'success': False, 'error': 'Invalid hobby IDs provided.'}, status=400)
        request.user.hobbies.add(*hobbies)
        return JsonResponse({'success': True, 'message': 'Hobbies added successfully.'}, status=200)

    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Failed to add hobbies.'}, status=500)
    

@login_required
def check_user_hobby(request):
    """
    This checks for users hobbies and ensures a certain specific hobby is present,then returns a success or error json response.
    """
    hobby_name = request.GET.get('hobby')
    if not hobby_name:
        return JsonResponse({'success': False, 'error': 'Hobby name is required.'}, status=400)

    try:
        hobby = Hobby.objects.filter(name=hobby_name).first()
        if not hobby:
            return JsonResponse({'success': False, 'error': 'Hobby does not exist in the database.'}, status=404)

        user_has_hobby = request.user.hobbies.filter(id=hobby.id).exists()
        return JsonResponse({'success': True, 'exists': user_has_hobby}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'An error occurred while checking the hobby.'}, status=500)
    
User = get_user_model()
def get_users(request):
    """
    Retrieve a paginated list of users filtered by age range and hobbies.
    """
    min_age = int(request.GET.get('min_age', 0))
    max_age = int(request.GET.get('max_age', 120))
    hobby = request.GET.get('hobby')

    """ Filter users by hobbies and age range"""
    users = User.objects.all()
    if hobby:
        users = users.filter(hobbies__name=hobby)
    if min_age or max_age:
        today = date.today()
        min_dob = today - timedelta(days=max_age * 365)
        max_dob = today - timedelta(days=min_age * 365)
        users = users.filter(dob__range=(min_dob, max_dob))

    """ this section Paginates the user list to leave 10 users per page"""
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

 
    user_data = [
        {
            "id": user.id,
            "username": user.username,
            "hobbies": list(user.hobbies.values_list('name', flat=True)),
        }
        for user in page
    ]

    return JsonResponse({'users': user_data, 'has_next': page.has_next()}, status=200)



@login_required
@require_http_methods(["DELETE"])
def remove_hobby(request):
    # Extract hobby name from GET or DELETE body
    if request.method == "DELETE":
        try:
            body = json.loads(request.body)
            hobby_name = body.get('hobby')  # Use 'hobby' key in DELETE body
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON payload.'}, status=400)

    if not hobby_name:
        return JsonResponse({'success': False, 'error': 'Hobby name is required.'}, status=400)

    try:
        # Find the hobby by name
        hobby = Hobby.objects.filter(name=hobby_name).first()
        if not hobby:
            return JsonResponse({'success': False, 'error': 'Hobby does not exist in the database.'}, status=404)

        # Check if the hobby is associated with the current user
        if not request.user.hobbies.filter(id=hobby.id).exists():
            return JsonResponse({'success': False, 'error': 'You do not have this hobby.'}, status=404)

        # Remove the hobby from the user's hobbies
        request.user.hobbies.remove(hobby)
        return JsonResponse({'success': True, 'message': f'Hobby "{hobby_name}" has been removed successfully.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'An error occurred: {str(e)}'}, status=500)
    

@login_required
def get_users_with_similar_hobbies(request):
    """
    Retrieve a paginated list of users with the most similar hobbies, filtered by age range.
    """
    current_user = request.user

    # Get filter parameters
    min_age = int(request.GET.get('min_age', 0))  
    max_age = int(request.GET.get('max_age', 300)) 

    # Calculate date of birth range
    today = date.today()
    min_dob = today - timedelta(days=max_age * 365)
    max_dob = today - timedelta(days=min_age * 365)

    # Get the current user's hobbies
    current_user_hobbies = current_user.hobbies.all()

    # Filter users
    users = (
        User.objects.exclude(id=current_user.id)  
        .filter(dob__range=(min_dob, max_dob))  
        .annotate(common_hobby_count=Count("hobbies", filter=Q(hobbies__in=current_user_hobbies)))
        .order_by("-common_hobby_count", "id") 
    )

    paginator = Paginator(users, 10)
    page_number = request.GET.get("page", 1)
    page = paginator.get_page(page_number)

    
    user_data = [
        {
            "id": user.id,
            "username": user.username,
            "common_hobby_count": user.common_hobby_count,
            "hobbies": list(user.hobbies.values_list("name", flat=True)),
        }
        for user in page
    ]
    return JsonResponse({"users": user_data, "has_next": page.has_next()}, status=200)