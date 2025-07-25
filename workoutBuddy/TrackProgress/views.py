import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def workout_log(request):
    token = request.session.get("token")
    if not token:
        messages.error(request, "Please login to view your workout plan.")
        return redirect("login")

    headers = {"Authorization": f"Bearer {token}"}
    
    if request.method == "POST":
        date = request.POST.get("selected_date")
        plan_id = request.POST.get("plan_id")
        status = request.POST.get("status", "completed")
        exercises_data = []

        for key in request.POST:
            if key.startswith("exercise_"):
                _, date_key, exercise_name = key.split("_", 2)
                completed = request.POST.get(key) == "on"
                sets = request.POST.get(f"sets_{exercise_name}", 0)
                reps = request.POST.get(f"reps_{exercise_name}", "")
                duration = request.POST.get(f"duration_{exercise_name}", "")
                
                exercises_data.append({
                    "name": exercise_name,
                    "sets": int(sets),
                    "reps": reps,
                    "duration_per_set": duration,
                    "completed": completed
                })

        payload = {
            "plan_id": plan_id,
            "date": date,
            "status": status,
            "created_at": timezone.now().isoformat(),
            "exercises": exercises_data
        }
        print(payload)

        try:
            response = requests.post("http://127.0.0.1:8000/api/workout/complete/", json=payload, headers=headers)
            response_data=response.json()
            print(response_data)
            if response_data['status'] == 201:
                messages.success(request, "Workout log submitted successfully.")
            else:
                messages.error(request, f"Failed to submit log: {response_data['message']}")
        except Exception as e:
            messages.error(request, f"Error: {e}")

        return redirect("workout_logger")  

    try:
        response = requests.get("http://127.0.0.1:8000/api/workout/plans/user", headers=headers)
        response_data = response.json()
        workout_plan = response_data.get("data", [None])[0]

        if workout_plan and "_id" in workout_plan:
            workout_plan["id"] = workout_plan.pop("_id")

    except Exception as e:
        workout_plan = None
        messages.error(request, f"Failed to load workout plan: {e}")

    return render(request, "workout_log.html", {"workout_plan": workout_plan})
