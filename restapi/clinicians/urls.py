from django.urls import path
from .views import clinicians_view

urlpatterns = [
    path('clinicians/', clinicians_view, name='clinicians'),
]