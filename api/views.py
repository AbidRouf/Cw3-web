from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, update_session_auth_hash, logout
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from datetime import datetime, date, timedelta
import json
from django.core.paginator import Paginator
from .models import Hobby, FriendRequest

User = get_user_model()

@login_required
def list_friend_requests(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        friend_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
        
        requests_data = [
            {
                "id": fr.id,
                "from_user_id": fr.from_user.id,
                "from_username": fr.from_user.username,
                "sent_on": fr.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "hobbies": list(fr.from_user.hobbies.values_list("name", flat=True))
            }
            for fr in friend_requests
        ]
        
        return JsonResponse({"friend_requests": requests_data}, safe=False, status=200)

@login_required
@require_POST
def send_friend_request(request: HttpRequest) -> JsonResponse:
    to_user_id = request.POST.get('to_user_id')
    if not to_user_id:
        return JsonResponse({'success': False, 'error': 'User ID is required.'}, status=400)

    try:
        to_user = User.objects.get(id=to_user_id)
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user, accepted=False).exists():
            return JsonResponse({'success': False, 'error': 'Friend request already sent and is still pending.'}, status=400)

        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return JsonResponse({'success': True, 'message': 'Friend request sent successfully.'}, status=201)

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_POST
def accept_friend_request(request: HttpRequest) -> JsonResponse:
    try:
        to_user_id = request.POST.get('to_user_id')
        if not to_user_id:
            return JsonResponse({'success': False, 'error': 'User ID is required.'}, status=400)

        friend_request = FriendRequest.objects.filter(
            from_user_id=to_user_id,
            to_user=request.user,
            accepted=False
        ).first()

        if not friend_request:
            return JsonResponse({'success': False, 'error': 'Friend request does not exist or already accepted.'}, status=404)

        friend_request.accepted = True
        friend_request.save()

        request.user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(request.user)

        return JsonResponse({'success': True, 'message': 'Friend request accepted successfully.'}, status=200)

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
        
@login_required
@require_POST
def remove_friend_request(request: HttpRequest) -> JsonResponse:
    try:
        to_user_id = request.POST.get('to_user_id')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON payload.'}, status=400)

    if not to_user_id:
        return JsonResponse({'success': False, 'error': 'User ID is required.'}, status=400)

    try:
        to_user = User.objects.get(id=to_user_id)
        friend_request = FriendRequest.objects.filter(from_user=to_user, to_user=request.user, accepted=False).first()
        if not friend_request:
            return JsonResponse({'success': False, 'error': 'Friend request does not exist.'}, status=400)

        friend_request.delete()
        return JsonResponse({'success': True, 'message': 'Friend request declined successfully.'}, status=200)

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
        
def signup_view(request: HttpRequest) -> HttpResponse:
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

def auth_status(request: HttpRequest) -> JsonResponse:
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
def profile_view(request: HttpRequest) -> JsonResponse:
    try:
        hobbies = list(request.user.hobbies.values())
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
def change_user_password(request: HttpRequest) -> JsonResponse:
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
def get_csrf_token(request: HttpRequest) -> JsonResponse:
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
def create_new_hobby(request: HttpRequest) -> JsonResponse:
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
        return JsonResponse({'success': False, 'error': 'An error while adding the hobby.'}, status=500)

@login_required
@require_POST
def update_profile(request: HttpRequest) -> JsonResponse:
    """
    For updating users profile details,then will return a succesfull response if all is added correctly or an error response if not added in intended way
    """
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    dob = request.POST.get('dob')
    username = request.POST.get('username')
    try:
        if first_name:
            request.user.first_name = first_name
        if last_name:
            request.user.last_name = last_name
        if email:
            request.user.email = email
        if dob:
            request.user.dob = datetime.strptime(dob, '%Y-%m-%d').date()
        if username:
            if request.user.username != username and User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'error': 'Username is already taken.'}, status=400)
            request.user.username = username
        request.user.save()
        return JsonResponse({'success': True, 'message': 'Profile updated successfully.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Failed to update profile.'}, status=500)

def get_all_hobbies(request: HttpRequest) -> JsonResponse:
    """
    fetches all hobbies all from the database,and will return a json response as seen on the last line
    """
    hobbies = list(Hobby.objects.values('id', 'name'))
    return JsonResponse({'success': True, 'hobbies': hobbies}, status=200)

def add_hobby(request: HttpRequest) -> JsonResponse:
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
def check_user_hobby(request: HttpRequest) -> JsonResponse:
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
def get_users(request: HttpRequest) -> JsonResponse:
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
def remove_hobby(request: HttpRequest) -> JsonResponse:
    """THIS FUNCTION is for removing the bobby from the hobby list and updating the page with the updated hobby list"""
    if request.method == "DELETE":
        try:
            body = json.loads(request.body)
            hobby_name = body.get('hobby')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON payload.'}, status=400)

    if not hobby_name:
        return JsonResponse({'success': False, 'error': 'Hobby name is required.'}, status=400)

    try:
        hobby = Hobby.objects.filter(name=hobby_name).first()
        if not hobby:
            return JsonResponse({'success': False, 'error': 'Hobby does not exist in the database.'}, status=404)

        if not request.user.hobbies.filter(id=hobby.id).exists():
            return JsonResponse({'success': False, 'error': 'You do not have this hobby.'}, status=404)

        request.user.hobbies.remove(hobby)
        return JsonResponse({'success': True, 'message': f'Hobby "{hobby_name}" has been removed successfully.'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'An error occurred: {str(e)}'}, status=500)
    

@login_required
def get_users_with_similar_hobbies(request: HttpRequest) -> JsonResponse:
    """
    Retrieves a paginated list of users with the most similar hobbies, filtered by age range
    """
    current_user = request.user

    min_age = int(request.GET.get('min_age', 0))  
    max_age = int(request.GET.get('max_age', 300)) 

    today = date.today()
    min_dob = today - timedelta(days=max_age * 365)
    max_dob = today - timedelta(days=min_age * 365)

    current_user_hobbies = current_user.hobbies.all()

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


@login_required
def show_friends(request: HttpRequest) -> JsonResponse:
    try:
        friends = request.user.friends.all()
        friends_data = [
            {"id": friend.id, "username": friend.username, "email": friend.email, "hobbies": list(friend.hobbies.values_list("name", flat=True))}
            for friend in friends
        ]
        return JsonResponse({"success": True, "friends": friends_data}, status=200)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)