from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.diet_preference_view, name='dietPreference'),
<<<<<<< HEAD
   path('result/<str:plan_id>/', views.diet_result_view, name='diet_result'),
=======
    path('result/', views.dietResult, name='dietResult'),
>>>>>>> 7c9735b (Initial local files before pulling Development branch)
    ]