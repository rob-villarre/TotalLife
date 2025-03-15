from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
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
    return Response(serializer.data, status=status.HTTP_200_OK)

def create_appointment(request):    
    
    serializer = AppointmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def appointment_view(request, appointment_id):

    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        return update_appointment(request=request, appointment=appointment)
    elif request.method == 'DELETE':
        return delete_appointment(request=request, appointment=appointment)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def delete_appointment(request, appointment):
    appointment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
 
def update_appointment(request, appointment):
    serializer = AppointmentSerializer(appointment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



