from django.urls import path
from .views import workout_log

urlpatterns = [
    path('log/', workout_log, name='workout_logger'),  # ✅ Fix: Name must match redirect
]
