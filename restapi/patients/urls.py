from django.urls import path
from .views import patients_view

urlpatterns = [
    path('patients/', patients_view, name='patients'),
]