from django.urls import path
from .views import appointments_view, appointment_view

urlpatterns = [
    path('appointments/', appointments_view, name='appointments'),
    path('appointments/<int:appointment_id>/', appointment_view, name='appointment_detail'),
]