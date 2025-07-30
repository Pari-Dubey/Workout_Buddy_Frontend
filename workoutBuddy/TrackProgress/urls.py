from django.urls import path
from .views import workout_log

urlpatterns = [
    path('workout/log/', workout_log, name='workout_logger'),
]
