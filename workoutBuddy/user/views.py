import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from datetime import datetime

FASTAPI_BASE_URL = 'http://localhost:8000'


def register_view(request):
    error_message = None  # To hold backend or request errors

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = {
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
                'oauth_provider': 'local',
            }
            try:
                response = requests.post(f'{FASTAPI_BASE_URL}/api/register', json=data)
                res_data = response.json()
                print(res_data.get("status"))
                if res_data.get("status") == 201:
                 return redirect('login') + '?show=login'
                else:
                    error_message = res_data.get("message", "Registration failed.")
            except requests.exceptions.RequestException as e:
                error_message = f"Request failed: {e}"
    else:
        form = RegisterForm()

    return render(request, 'login-signup.html', {'form': form, 'register_error': error_message})


def login_view(request):
    error_message = None
    show_login = request.GET.get('show') == 'login'

    if request.method == 'POST' and request.POST.get('form_type') == 'login':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = {
                'username': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
            }
            try:
                response = requests.post(
                    f'{FASTAPI_BASE_URL}/api/login',
                    data=data,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'}
                )
                user_data = response.json()

                if 'access_token' in user_data:
                    token = user_data.get("access_token")
                    request.session['token'] = token
                    return redirect('profile')  
                else:
                    error_message = user_data.get('detail') or user_data.get('message') or "Login failed."

            except Exception as e:
                print("Login error:", str(e))
                error_message = "Please try again later."
        else:
            error_message = "Please correct the errors below."
    else:
        form = LoginForm()

        return render(request, 'login-signup.html', {
        'form': form,
        'login_error': error_message,
        'show_login': show_login 
    })



def google_login_redirect(request):
    return redirect(f'{FASTAPI_BASE_URL}/auth/google/login')


def google_login_callback(request):
    token = request.GET.get('token')
    user_id = request.GET.get('user_id')

    if token and user_id:
        request.session['token'] = token
        request.session['user_id'] = user_id
        messages.success(request, "Google login successful!")
        return redirect('profile')
    else:
        messages.error(request, "Google login failed: Missing credentials.")
        return redirect('login')

def view_profile(request):
    token = request.session.get("token")
    if not token:
         return redirect("flip_login_signup") 

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/api/user/profile", headers=headers)

        if response.status_code == 200:
            json_data = response.json()
            if not json_data or 'data' not in json_data or json_data['data'] is None:
                # This is actually a new user or bad response
                return redirect('create_profile')

            profile_data = json_data['data']

            created_at_str = profile_data.get('created_at')
            if created_at_str:
                try:
                    profile_data['created_at'] = datetime.fromisoformat(created_at_str)
                except ValueError:
                    profile_data['created_at'] = None

            return render(request, 'view-profile.html', {'profile': profile_data})
        
        else:
            messages.error(request, "Error fetching profile.")
            return redirect("flip_login_signup")

    except requests.exceptions.RequestException:
        messages.error(request, "Connection error.")
        return redirect("flip_login_signup")
      
    except requests.exceptions.RequestException:
        messages.error(request, "Connection error.")
        return redirect("login")

def create_profile(request):
    token = request.session.get('token')

    if not token:
        messages.error(request, "You must be logged in to create a profile.")
        return redirect('login') 

    headers = {'Authorization': f'Bearer {token}'}

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)

            try:
                response = requests.post(
                    f'{FASTAPI_BASE_URL}/api/user/profile',
                    headers=headers,
                    json=data
                )
                if response.status_code in [200, 201]:
                    messages.success(request, "Profile created successfully!")
                    return redirect('profile') 
                else:
                    error_detail = response.json().get("detail", response.text)
                    messages.error(request, f"Failed to create profile: {error_detail}")
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Server error: {str(e)}")
        else:
            messages.error(request, "Form validation failed.")
    else:
        form = ProfileForm()

    return render(request, 'create-profile.html', {'form': form})


def edit_profile(request):
    token = request.session.get('token')
    if not token:
        messages.error(request, "You must be logged in to edit a profile.")
        return redirect('login')

    headers = {'Authorization': f'Bearer {token}'}
    profile_data = {}

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            try:
                response = requests.patch(
                    f'{FASTAPI_BASE_URL}/api/user/profile',
                    headers=headers,
                    json=form.cleaned_data
                )
                if response.status_code == 200:
                    # messages.success(request, "Profile updated successfully.")
                    return redirect('profile')
                else:
                    error_detail = response.json().get("detail", "Unknown error")
                    messages.error(request, f"Failed to update profile: {error_detail}")
            except requests.RequestException as e:
                messages.error(request, f"Server error: {str(e)}")
        # If form is invalid, we keep the same form and show errors

    else:  # GET request
        try:
            response = requests.get(f'{FASTAPI_BASE_URL}/api/user/profile', headers=headers)
            if response.status_code == 200:
                profile_data = response.json().get("data", {})
        except requests.RequestException as e:
            messages.error(request, f"Server is unavailable: {str(e)}")
            return redirect('profile')

        form = ProfileForm(initial=profile_data)

    return render(request, 'edit-profile.html', {
        'form': form,
        'profile_data': profile_data  
    })

def flip_login_signup(request):
    return render(request, 'login-signup.html')