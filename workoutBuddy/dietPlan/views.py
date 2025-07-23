<<<<<<< HEAD
from django.shortcuts import render, redirect
import requests

FASTAPI_BASE_URL = 'http://localhost:8000'


def diet_preference_view(request):
    allergies_list = ['Nuts', 'Gluten', 'Dairy', 'Soy', 'Eggs', 'Shellfish', 'None']

    # Ensure user is authenticated
    token = request.session.get('token')
    if not token:
        return redirect('login')

    # Get user_id from session or fetch via token
    user_id = request.session.get('user_id')
    if not user_id:
        try:
            headers = {'Authorization': f'Bearer {token}'}
            resp = requests.get(f'{FASTAPI_BASE_URL}/api/user/profile', headers=headers)
            if resp.status_code == 200:
                user_data = resp.json().get('data', {})
                user_id = user_data.get('user_id')
                if user_id:
                    request.session['user_id'] = user_id
            else:
                print("[DEBUG] Could not fetch user profile:", resp.text)
        except Exception as e:
            print(f"[ERROR] Failed to fetch user_id: {e}")

    if not user_id:
        return redirect('login')

    # Handle POST submission
    if request.method == 'POST':
        try:
            #  Extract form fields
            diet_type = request.POST.get('diet_type')
            activity_level = request.POST.get('activity_level')
            fitness_goal = request.POST.get('fitness_goal')
            experience_level = request.POST.get('experience_level')
            medical_conditions = request.POST.get('medical_conditions', '')
            past_injuries = request.POST.get('past_injuries', '')
            preferred_workout_style = request.POST.get('preferred_workout_style')
            preferred_training_days = request.POST.get('preferred_training_days')

            # Convert to integer safely
            try:
                preferred_training_days = int(preferred_training_days)
            except (ValueError, TypeError):
                preferred_training_days = 3

            # Handle allergies
            allergies = request.POST.getlist('allergies') or []
            other_allergy = request.POST.get('other_allergy', '').strip()
            if other_allergy:
                allergies.append(other_allergy)

            #  Prepare payload to send to FastAPI
            payload = {
                "diet_type": diet_type,
                "activity_level": activity_level,
                "fitness_goal": fitness_goal,
                "experience_level": experience_level,
                "medical_conditions": [m.strip() for m in medical_conditions.split(',') if m.strip()],
                "allergies": allergies,
                "other_allergy": other_allergy,
                "preferred_workout_style": preferred_workout_style,
                "preferred_training_days_per_week": preferred_training_days
            }

            #  POST to FastAPI
            response = requests.post(
                f"{FASTAPI_BASE_URL}/diet/generate-diet-plan/{user_id}",
                json=payload
            )

            #  Redirect to result page with plan_id if successful
            print(response.status_code)
            if response.status_code == 200 or 201:
                data = response.json().get("data", {})
                plan_id = data['diet_plan_id']

                if plan_id:
                    return redirect('dietPlan:diet_result', plan_id=plan_id)
                else:
                    print("[DEBUG] Plan created but no ID returned.")
            else:
                print("[DEBUG] FastAPI error:", response.text)

        except Exception as e:
            print(f"[ERROR] Form processing failed: {e}")

    # ⬅ On GET request, render the form
    return render(request, 'diet-form.html', {
        'allergies_list': allergies_list
    })


def diet_result_view(request, plan_id):
    # Ensure user is authenticated
    token = request.session.get('token')
    if not token:
        return redirect('login')

    try:
        #  Fetch saved plan from FastAPI using the plan_id
        response = requests.get(f"{FASTAPI_BASE_URL}/diet/diet-plan/{plan_id}")

        if response.status_code == 200:
            data = response.json().get("data", {})
            plan = data.get("ai_generated_plan", {})  # Should be a dict of day: meals
        else:
            print("[DEBUG] Failed to fetch diet plan:", response.text)
            plan = {}
    except Exception as e:
        print(f"[ERROR] Could not fetch diet result: {e}")
        plan = {}

    return render(request, 'diet-result.html', {
        'diet_plan': plan
    })
=======
# views.py
from django.shortcuts import render,redirect
from .forms import DietPreferenceForm
import requests
import json

def diet_preference_view(request):
    allergies_list = ['Nuts', 'Gluten', 'Dairy', 'Soy', 'Eggs', 'Shellfish', 'None']
    diet_plan = None
    form = DietPreferenceForm(request.POST)
    # if request.method == 'POST':
    #     form = DietPreferenceForm(request.POST)
    #     if form.is_valid():
    #         cleaned_data = form.cleaned_data

    #         # Fix: allergies field comes as list, ensure it's JSON serializable
    #         if "allergies" not in cleaned_data or cleaned_data["allergies"] is None:
    #             cleaned_data["allergies"] = []

    #         try:
    #             response = requests.post(
    #                 "http://127.0.0.1:8000/generate-diet-plan",
    #                 json=cleaned_data
    #             )
    #             if response.status_code == 200:
    #                 diet_plan = response.json().get("diet_plan")
    #                  # ✅ Store diet_plan in session and redirect
    #                 request.session['diet_plan'] = json.dumps(diet_plan)
    #                 return redirect('dietPlan:diet_result')
    #                   # 🔁 redirect instead of rendering on same page
    #             else:
    #                 form.add_error(None, "Error getting diet plan from API.")
    #         except Exception as e:
    #             form.add_error(None, f"Error connecting to backend: {e}")

    # else:
    #     form = DietPreferenceForm()

    return render(request, 'diet-form.html', {'form': form,'allergies_list':allergies_list})


#  NEW VIEW:
# def diet_result_view(request):
#     diet_plan_json = request.session.get('diet_plan')
#     if not diet_plan_json:
#         return redirect('diet-form')  # ⛔ if someone directly visits the result page

#     diet_plan = json.loads(diet_plan_json)
#     return render(request, 'diet-result.html', {'diet_plan': diet_plan})


def dietResult(request):
    return render(request,'diet-result.html')
>>>>>>> 7c9735b (Initial local files before pulling Development branch)
