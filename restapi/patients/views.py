from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Patient
from .serializer import PatientSerializer

@api_view(['GET'])
def get_patients(request):

    patient = {'name': 'Roberto'}
    serializer = PatientSerializer(patient)
    
    return Response(serializer.data)
