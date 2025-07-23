import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm

FASTAPI_BASE_URL = 'http://localhost:8000'


def register_view(request):
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
                if res_data.get("status") == 201:
                    messages.success(request, res_data["message"])
                    return redirect('login')
                else:
                    messages.error(request, res_data.get("message", "Registration failed."))
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Request failed: {e}")
    else:
        form = RegisterForm()
    return render(request, 'login-signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
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
                if response.status_code == 200:
                    user_data = response.json()
                    print(user_data)
                    token = user_data.get("access_token")
                    request.session['token'] = token
                    messages.success(request, "Login successful")
                    return redirect('profile')
                else:
                    error_detail = response.json().get('detail', 'Invalid credentials')
                    messages.error(request, f"Login failed: Login Required")
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Login request failed: {e}")
    else:
        form = LoginForm()
    return render(request, 'login-signup.html', {'form': form})


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
        messages.error(request, "You must be logged in to view your profile.")
        return redirect('login') 

    headers = {'Authorization': f'Bearer {token}'}

    try:
        response = requests.get(f'{FASTAPI_BASE_URL}/api/user/profile', headers=headers)

        if response.status_code == 200:
            profile_data = response.json().get("data", {})
            messages.success(request, "Profile fetched successfully.")
            return render(request, 'view-profile.html', {'profile': profile_data})

        messages.error(request, "Profile not found or couldn't be fetched.")
        return redirect('profile_form')

    except requests.exceptions.RequestException:
        messages.error(request, "The server is currently unavailable. Please try again later.")
        return render(request, 'create-profile.html', {
            'form': ProfileForm(),
            'is_editing': False
        })


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

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            try:
                response = requests.patch(  # Use PATCH as your FastAPI endpoint expects it
                    f'{FASTAPI_BASE_URL}/api/user/profile',
                    headers=headers,
                    json=data
                )
                if response.status_code == 200:
                    messages.success(request, "Profile updated successfully!")
                    return redirect('profile')
                else:
                    error_detail = response.json().get("detail", response.text)
                    messages.error(request, f"Failed to update profile: {error_detail}")
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Server error: {str(e)}")
                return redirect('edit_profile')
        else:
            messages.error(request, "Form validation failed. Please check the fields.")
    else:
        try:
            response = requests.get(f'{FASTAPI_BASE_URL}/api/user/profile', headers=headers)
            if response.status_code == 200:
                profile_data = response.json().get("data", {})
                form = ProfileForm(initial=profile_data)
            else:
                messages.error(request, "Could not load your profile for editing.")
                return redirect('profile')
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Server is unavailable: {str(e)}")
            return redirect('profile')

    return render(request, 'edit-profile.html', {'form': form})

def flip_login_signup(request):
    return render(request, 'login-signup.html')