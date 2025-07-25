import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from datetime import datetime
from django.http import JsonResponse
FASTAPI_BASE_URL = 'http://localhost:8000'


def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
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
                    return redirect('login')
                else:
                    form.add_error(None, res_data.get("message", "Registration failed."))
            except requests.exceptions.RequestException as e:
                form.add_error(None, f"Request failed: {e}")

    return render(request, 'login-signup.html', {'form': form, 'show_signup': True})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = {
                'username': form.cleaned_data['email'],  # OAuth2PasswordRequestForm uses 'username'
                'password': form.cleaned_data['password'],
            }
            try:
                response = requests.post(
                    f'{FASTAPI_BASE_URL}/api/login',
                    data=data,  # send as form data
                    headers={'Content-Type': 'application/x-www-form-urlencoded'}
                )
                if response.status_code == 200:
                    user_data = response.json()
                    print(user_data)
                    token = user_data.get("access_token")
                    request.session['token'] = token
                    return redirect('profile')
                else:
                    form.add_error(None, "Invalid email or password.")
            except requests.exceptions.RequestException as e:
                form.add_error(None, f"Login request failed: {e}")
    else:
        form = LoginForm()
    return render(request, 'login-signup.html', {'form': form , 'show_signup': False})

def password_flow_view(request):
    error = ""
    success = ""
    token = request.GET.get("token") or request.POST.get("token")

    if request.method == "POST":
        if token: 
            password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if password != confirm_password:
                error = "Passwords do not match."
                return render(request, "forgot-password.html", {"token": token, "error": error})

            response = requests.post(
                f'{FASTAPI_BASE_URL}/reset-password',
                data={"token": token, "new_password": password}
            )

            if response.status_code == 200:
                success = "Password reset successful. Please log in."
                return render(request, "forgot-password.html", {"success": success})
            else:
                try:
                    error_data = response.json()
                    error = error_data.get("message", "Failed to reset password.")
                except ValueError:
                    error = "Something went wrong. Could not process server response."

        else: 
            email = request.POST.get("email")
            if not email:
                error = "Email is required."
                return render(request, "forgot-password.html", {"error": error})

            response = requests.post(
                f'{FASTAPI_BASE_URL}/forgot-password',
                json={"email": email}
            )

            if response.status_code == 200:
                success = "If the email exists, a reset link has been sent."
            else:
                try:
                    error = response.json().get("message", "Failed to send reset link.")
                except ValueError:
                    error = "Could not contact the server."

    return render(request, "forgot-password.html", {"token": token, "error": error, "success": success})

def logout_view(request):
    request.session.flush() 
    messages.success(request, "Logged out successfully.")
    return redirect('login')

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
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/api/user/profile", headers=headers)

        if response.status_code == 200:
            json_data = response.json()
            if not json_data or 'data' not in json_data or json_data['data'] is None:
                return redirect('create_profile')  # No profile exists yet

            profile_data = json_data['data']

            # Format created_at if it exists
            created_at_str = profile_data.get('created_at')
            if created_at_str:
                try:
                    profile_data['created_at'] = datetime.fromisoformat(created_at_str)
                except ValueError:
                    profile_data['created_at'] = None

            # Fill form with initial values
            form = ProfileForm(initial={
                'full_name': profile_data.get('full_name', ''),
                'age': profile_data.get('age', ''),
                'gender': profile_data.get('gender', ''),
                'height': profile_data.get('height', ''),
                'weight': profile_data.get('weight', ''),
                'activity_level': profile_data.get('activity_level', ''),
                'goal': profile_data.get('goal', ''),
            })

            return render(request, 'view-profile.html', {
                'form': form,
                'profile': profile_data,
                'is_editing': True
            })


        else:
            messages.error(request, "Error fetching profile.")
            return redirect("login")

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
        return JsonResponse({'success': False, 'message': "Not authenticated"}, status=403)

    headers = {'Authorization': f'Bearer {token}'}

    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        form = ProfileForm(data)

        if form.is_valid():
            try:
                response = requests.patch(
                    f'{FASTAPI_BASE_URL}/api/user/profile',
                    headers=headers,
                    json=form.cleaned_data
                )

                if response.status_code == 200:
                    return JsonResponse({'success': True})
                else:
                    error_detail = response.json().get("detail", "Unknown error")
                    return JsonResponse({'success': False, 'message': error_detail})
            except requests.RequestException as e:
                return JsonResponse({'success': False, 'message': str(e)})

        return JsonResponse({'success': False, 'message': 'Invalid form data'})

    return JsonResponse({'success': False, 'message': 'Only POST allowed'}, status=405)
