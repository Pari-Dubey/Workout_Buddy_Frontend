from django.urls import path
from . import views

app_name = 'dietPlan'

urlpatterns = [
    path('', views.diet_preference_view, name='dietPreference'),
    path('diet-result/<str:plan_id>/', views.diet_result_view, name='diet_result'),
    path('meal-log/', views.meal_log_view, name='meal_log'),
    path('submit-meal-log/', views.submit_meal_log_view, name='submit_meal_log'),
    
]
