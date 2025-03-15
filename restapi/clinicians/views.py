from django.shortcuts import render

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Clinician
from .serializer import ClinicianSerializer
import requests


@api_view(['GET', 'POST'])
def clinicians_view(request):
    if request.method == 'GET':
        return get_clinicians(request=request)
    elif request.method == 'POST':
        return create_clinician(request=request)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def get_clinicians(request):
    clinicians = Clinician.objects.all()
    serializer = ClinicianSerializer(clinicians, many=True)
    return Response(serializer.data)

def create_clinician(request):

    # required_fields = [field.name for field in Clinician._meta.get_fields()]
    # missing_fields = [field for field in required_fields if field not in request.POST]

    # if missing_fields:
    #     return Response({'error': f'Missing required fields: {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)


    if not validate_clinician(request.data['npi_number'], request.data['first_name'], request.data['last_name'], request.data['state']):
        return Response({'error': 'Clinician could not be validated with the NPI number'}, status=status.HTTP_400_BAD_REQUEST)
    
    Clinician.objects.create(
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            npi_number=request.data['npi_number'],
            state=request.data['state']
        )
    serializer = ClinicianSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def validate_clinician(npi_number, first_name, last_name, state):
    # API endpoint for NPI validation
    url = f'https://npiregistry.cms.hhs.gov/api/?number={npi_number}&version=2.1'

    response = requests.get(url)

    if response.status_code != 200:
        return False
    
    data = response.json()

    if 'results' not in data or len(data['results']) == 0:
        return False
    
    clinician_data = data['results'][0]
    # TODO: check all addresses?
    if clinician_data['basic']['first_name'] != first_name \
        or clinician_data['basic']['last_name'] != last_name \
        or clinician_data['addresses'][0]['state'] != state:
        return False
    
    return True
    
    


