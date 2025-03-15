from django.urls import path
from .views import patients_view, patient_view

urlpatterns = [
    path('patients/', patients_view, name='patients'),
    path('patients/<int:patient_id>/', patient_view, name='patient_detail'),
]