from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Patient
from .serializer import PatientSerializer


@api_view(['GET', 'POST'])
def patients_view(request):
    if request.method == 'GET':
        return get_patients(request=request)
    elif request.method == 'POST':
        return create_patient(request=request)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def get_patients(request):
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)

def create_patient(request):
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def patient_view(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
    elif request.method == 'PUT':
        return update_patient(request=request, patient=patient)
    elif request.method == 'DELETE':
        return delete_patient(request=request, patient=patient)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
def delete_patient(request, patient):
    patient.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

def update_patient(request, patient):
    serializer = PatientSerializer(patient, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
