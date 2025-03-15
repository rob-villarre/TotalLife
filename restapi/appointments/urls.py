from django.urls import path
from .views import appointments_view

urlpatterns = [
    path('appointments/', appointments_view, name='appointments'),
]