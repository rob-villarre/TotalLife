from django.shortcuts import render

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import clinician
from .serializer import clinicianSerializer


@api_view(['GET', 'POST'])
def clinicians_view(request):
    if request.method == 'GET':
        return get_clinicians(request=request)
    elif request.method == 'POST':
        return create_clinician(request=request)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def get_clinicians(request):
    clinicians = clinician.objects.all()
    serializer = clinicianSerializer(clinicians, many=True)
    return Response(serializer.data)

def create_clinician(request):
    serializer = clinicianSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
