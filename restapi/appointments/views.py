from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from clinicians.models import Clinician
from patients.models import Patient
from .models import Appointment
from .serializer import AppointmentSerializer

@api_view(['GET', 'POST'])
def appointments_view(request):
    if request.method == 'GET':
        return get_appointments(request=request)
    elif request.method == 'POST':
        return create_appointment(request=request)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def get_appointments(request):
    appointments = Appointment.objects.all()
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)

def create_appointment(request):
    patient_id =  request.data.get('patient')
    clinician_id = request.data.get('clinician')
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')
    appointment_status = request.data.get('status')

    if not patient_id or not clinician_id or not start_date or not end_date or not appointment_status:
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        clinician = Clinician.objects.get(id=clinician_id)
    except Clinician.DoesNotExist:
        return Response({'error': 'Clinician not found'}, status=status.HTTP_404_NOT_FOUND)
    
    appointment = {
        "patient": patient.pk,
        "clinician": clinician.pk,
        "start_date": start_date,
        "end_date": end_date,
        "status": appointment_status
    }
    
    serializer = AppointmentSerializer(data=appointment)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.messages, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


