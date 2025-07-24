from django.shortcuts import render, redirect
import requests

FASTAPI_BASE_URL = 'http://localhost:8000'


# ===================== DIET PREFERENCE =====================

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
            # Extract form fields
            diet_type = request.POST.get('diet_type')
            activity_level = request.POST.get('activity_level')
            fitness_goal = request.POST.get('fitness_goal')
            experience_level = request.POST.get('experience_level')
            medical_conditions = request.POST.get('medical_conditions', '')
           
            preferred_workout_style = request.POST.get('preferred_workout_style')
            preferred_training_days = request.POST.get('preferred_training_days')

            try:
                preferred_training_days = int(preferred_training_days)
            except (ValueError, TypeError):
                preferred_training_days = 3  # default fallback

            # Handle allergies
            allergies = request.POST.getlist('allergies') or []
            other_allergy = request.POST.get('other_allergy', '').strip()
            if other_allergy:
                allergies.append(other_allergy)

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

            # POST to FastAPI
            headers = {'Authorization': f'Bearer {token}'}

            response = requests.post(
            f"{FASTAPI_BASE_URL}/diet/generate-diet-plan/",
            json=payload,
            headers=headers
)

            

            print("[DEBUG] FastAPI status:", response.status_code)
            print("[DEBUG] FastAPI raw response:", response.text)

            if response.status_code in [200, 201]:
                try:
                    data = response.json().get("data", {})
                    print("[DEBUG] FastAPI response JSON:", data)

                    plan_id = data.get('diet_plan_id')
                    if plan_id:
                        return redirect('dietPlan:diet_result', plan_id=plan_id)
                    else:
                        print("[DEBUG] Plan created but no diet_plan_id returned:", data)
                except Exception as e:
                    print(f"[ERROR] Failed to parse response JSON: {e}")
            else:
                print("[DEBUG] FastAPI returned error:", response.text)

        except Exception as e:
            print(f"[ERROR] Form processing failed: {e}")

    return render(request, 'diet-form.html', {
        'allergies_list': allergies_list
    })


# ===================== DIET RESULT =====================

def diet_result_view(request, plan_id):
    token = request.session.get('token')
    if not token:
        return redirect('login')

    try:
       headers = {'Authorization': f'Bearer {token}'}
       response = requests.get(f"{FASTAPI_BASE_URL}/diet/diet-plan/{plan_id}", headers=headers)

       print(f"[DEBUG] Fetching diet plan {plan_id} - status: {response.status_code}")

       if response.status_code == 200:
            data = response.json().get("data", {})
            print("[DEBUG] Diet plan data:", data)
            plan = data.get("ai_generated_plan", {})
       else:
            print("[DEBUG] Failed to fetch diet plan:", response.text)
            plan = {}
    except Exception as e:
        print(f"[ERROR] Could not fetch diet result: {e}")
        plan = {}

    return render(request, 'diet-result.html', {
        'diet_plan': plan
    })


# ===================== MEAL LOG =====================

def meal_log_view(request):
    token = request.session.get('token')
    if not token:
        return redirect('login')

    meal_types = ['breakfast', 'lunch', 'dinner']

    return render(request, 'meal-log.html', {
        'meal_types': meal_types
    })


def submit_meal_log_view(request):
    if request.method == 'POST':
        token = request.session.get('token')
        date = request.POST.get('date')
        meal_data = {'date': date, 'breakfast': [], 'lunch': [], 'dinner': []}

        for meal_type in ['breakfast', 'lunch', 'dinner']:
            items = []
            for key in request.POST:
                if key.startswith(f"{meal_type}["):
                    idx = key[len(meal_type) + 1:].split(']')[0]
                    field = key.split('[')[2].rstrip(']')
                    if idx.isdigit():
                        idx = int(idx)
                        while len(items) <= idx:
                            items.append({})
                        items[idx][field] = request.POST[key]

            for item in items:
                item_data = {
                    "item_name": item.get("item_name"),
                    "quantity": float(item.get("quantity")) if item.get("quantity") else None,
                    "weight_in_grams": float(item.get("weight_in_grams")) if item.get("weight_in_grams") else None
                }
                if item_data["item_name"]:
                    meal_data[meal_type].append(item_data)

        meal_data = {k: v for k, v in meal_data.items() if v or k == "date"}

        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.post(f"{FASTAPI_BASE_URL}/api/progress/meal-log/", json=meal_data,headers=headers)

            print("[DEBUG] Meal log POST status:", response.status_code)
            print("[DEBUG] Meal log response:", response.text)

            if response.status_code in [200, 201]:
                return render(request, "meal-log.html", {"message": "Meal log submitted successfully!"})
            else:
                return render(request, "meal-log.html", {"message": "Failed to log meal."})

        except Exception as e:
            print(f"[ERROR] Meal log submission failed: {e}")
            return render(request, "meal-log.html", {"message": "Error submitting meal log."})

    return redirect('meal_log')