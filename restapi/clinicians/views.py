from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Clinician
from .serializer import ClinicianSerializer


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
    
    serializer = ClinicianSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def clinician_view(request, clinician_id):
    try:
        clinician = Clinician.objects.get(id=clinician_id)
    except Clinician.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ClinicianSerializer(clinician)
        return Response(serializer.data)
    elif request.method == 'PUT':
        return update_clinician(request=request, clinician=clinician)
    elif request.method == 'DELETE':
        return delete_clinician(request=request, clinician=clinician)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def delete_clinician(request, clinician):
    clinician.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

def update_clinician(request, clinician):
    serializer = ClinicianSerializer(clinician, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


