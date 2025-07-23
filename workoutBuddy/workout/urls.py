from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('create/', views.create_workout_view, name='create_workout'),
    path('plan/', views.workout_plan_view, name='workout_plan'),
    path('view/', views.view_workout_view, name='view_workout'),
    path('', views.workout_plan_view, name='home'), # Optional: make workout plan the default
=======
    path("create/", views.create_workout_plan, name="create_workout_plan"),
    path("view/", views.view_workout_plan, name="view_workout_plan"),
>>>>>>> 7c9735b (Initial local files before pulling Development branch)
]
