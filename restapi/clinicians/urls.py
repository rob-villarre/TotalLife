from django.urls import path
from .views import clinicians_view, clinician_view

urlpatterns = [
    path('clinicians/', clinicians_view, name='clinicians'),
    path('clinicians/<int:clinician_id>/', clinician_view, name='clinician_detail'),
]