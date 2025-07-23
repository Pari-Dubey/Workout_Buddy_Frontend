from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.diet_preference_view, name='dietPreference'),
   path('result/<str:plan_id>/', views.diet_result_view, name='diet_result'),
    ]