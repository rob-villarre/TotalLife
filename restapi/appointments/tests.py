from rest_framework.test import APITestCase
from rest_framework import status

from .models import Appointment
from patients.models import Patient
from clinicians.models import Clinician

class AppointmentAPITests(APITestCase):
    def setUp(self):
        self.url = '/api/appointments/'

        self.patient_one = {
            'first_name': 'Bob',
            'last_name': 'Smith',
            'dob': '1990-01-01',
            'email': 'john.doe@example.com',
            'phone_number': '1234567890',
        }
        patient = Patient.objects.create(**self.patient_one)
        self.patient_one['id'] = patient.id

        self.patient_two = {
            'first_name': 'Bob2',
            'last_name': 'Smith2',
            'dob': '1990-01-01',
            'email': 'john.doe2@example.com',
            'phone_number': '1234567890',
        }
        patient = Patient.objects.create(**self.patient_two)
        self.patient_two['id'] = patient.id

        self.clinician_one = {
            'first_name': 'Bob',
            'last_name': 'Smith',
            'npi_number': '1234567890',
            'state': 'CA',
        }
        clinician = Clinician.objects.create(**self.clinician_one)
        self.clinician_one['id'] = clinician.id

        self.clinician_two = {
            'first_name': 'Mark',
            'last_name': 'Tom',
            'npi_number': '0987654321',
            'state': 'AB',
        }
        clinician = Clinician.objects.create(**self.clinician_two)
        self.clinician_two['id'] = clinician.id

        # valid appointment json to use
        self.appointment = {
            'patient': self.patient_one['id'],
            'clinician': self.clinician_one['id'],
            'start_date': '2021-01-01T10:00:00Z',
            'end_date': '2021-01-01T11:00:00Z',
            'status': 'SCHEDULED'
        }

        return super().setUp()
    
    def test_create_appointment(self):
        response = self.client.post(self.url, self.appointment, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['patient'], self.appointment['patient'])
        self.assertEqual(response.data['clinician'], self.appointment['clinician'])
        self.assertEqual(response.data['start_date'], self.appointment['start_date'])
        self.assertEqual(response.data['end_date'], self.appointment['end_date'])
        self.assertEqual(response.data['status'], self.appointment['status'])

    def test_create_appointment_missing_field(self):
        appointment = {
            'patient': self.patient_one['id'],
            'clinician': self.clinician_one['id'],
            'appointment_date': '2021-01-01',
            'end_date': '2021-01-01T11:00:00Z',
        }

        response = self.client.post(self.url, appointment, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['start_date'], ['This field is required.'])
    
    def test_create_appointment_with_overlappping_time(self):
        response = self.client.post(self.url, self.appointment, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.appointment['patient'] = 2
        self.appointment['start_date'] = '2021-01-01T10:30:00Z'
        response = self.client.post(self.url, self.appointment, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This appointment overlaps with an existing appointment for the clinician.', response.data['non_field_errors'])

    def test_get_appointments(self):
        response = self.client.post(self.url, self.appointment, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['patient'], self.appointment['patient'])
        self.assertEqual(response.data[0]['clinician'], self.appointment['clinician'])
        self.assertEqual(response.data[0]['start_date'], self.appointment['start_date'])
        self.assertEqual(response.data[0]['end_date'], self.appointment['end_date'])
        self.assertEqual(response.data[0]['status'], self.appointment['status'])
    
    def test_get_appointment(self):
        response = self.client.post(self.url, self.appointment, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        appointment_id = response.data['id']

        response = self.client.get(self.url + str(appointment_id) + '/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['patient'], self.appointment['patient'])
        self.assertEqual(response.data['clinician'], self.appointment['clinician'])
        self.assertEqual(response.data['start_date'], self.appointment['start_date'])
        self.assertEqual(response.data['end_date'], self.appointment['end_date'])
        self.assertEqual(response.data['status'], self.appointment['status'])

    def test_delete_appointment(self):
        response = self.client.post(self.url, self.appointment, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        appointment_id = response.data['id']

        response = self.client.delete(self.url + str(appointment_id) + '/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(self.url + str(appointment_id) + '/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_appointment(self):
        response = self.client.post(self.url, self.appointment, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        appointment_id = response.data['id']

        self.appointment['status'] = 'COMPLETED'
        response = self.client.put(self.url + str(appointment_id) + '/', self.appointment, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['patient'], self.appointment['patient'])
        self.assertEqual(response.data['clinician'], self.appointment['clinician'])
        self.assertEqual(response.data['start_date'], self.appointment['start_date'])
        self.assertEqual(response.data['end_date'], self.appointment['end_date'])
        self.assertEqual(response.data['status'], self.appointment['status'])

    def test_update_appointment_with_overlapppping_time(self):
        response = self.client.post(self.url, self.appointment, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.appointment['clinician'] = 2
        self.appointment['start_date'] = '2021-01-01T08:00:00Z'
        self.appointment['end_date'] = '2021-01-01T09:00:00Z'

        response = self.client.post(self.url, self.appointment, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        appointment_two_id = response.data['id']

        # overlaping appointment
        self.appointment['end_date'] = '2021-01-01T12:00:00Z'
        response = self.client.put(self.url + str(appointment_two_id) + '/', self.appointment, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This appointment overlaps with an existing appointment for the patient.', response.data['non_field_errors'])
    