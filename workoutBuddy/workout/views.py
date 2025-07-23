import json
from django.shortcuts import render
from django.http import HttpResponse

# Mock data for the workout plan
# In a real application, this data would come from a database or an external API
def create_workout_view(request):
    """
    Renders the create workout page.
    """
    return render(request, 'create-workout.html')





def workout_plan_view(request):
    return render(request, 'workout-plan.html', context)


def view_workout_view(request):
    """
    Renders the view workout page.
    """
    return render(request, 'view-workout.html')
