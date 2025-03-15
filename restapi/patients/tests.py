from rest_framework.test import APITestCase
from .models import Patient
from rest_framework import status

class PatientsAPITests(APITestCase):
    def setUp(self):
        self.url = '/api/patients/'
        return super().setUp()
    
    def test_create_patient(self):
        patient = {
            'first_name': 'Bob',
            'last_name': 'Smith',
            'dob': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'bob.smith@example.com',
            'gender': 'Male'
        }
        
        response = self.client.post(self.url, patient, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], patient['first_name'].upper())
        self.assertEqual(response.data['last_name'], patient['last_name'].upper())
        self.assertEqual(response.data['dob'], patient['dob'])
        self.assertEqual(response.data['phone_number'], patient['phone_number'])
        self.assertEqual(response.data['email'], patient['email'].lower())
        self.assertEqual(response.data['gender'], patient['gender'].upper())
        
        patient_id = response.data['id']
        patient_db = Patient.objects.get(id=patient_id)
        self.assertEqual(patient_db.first_name, patient['first_name'].upper())
        self.assertEqual(patient_db.last_name, patient['last_name'].upper())
        self.assertEqual(patient_db.dob.strftime('%Y-%m-%d'), patient['dob'])
        self.assertEqual(patient_db.phone_number, patient['phone_number'])
        self.assertEqual(patient_db.email, patient['email'].lower())
        self.assertEqual(patient_db.gender, patient['gender'].upper())
    
    def test_create_patient_with_invalid_email(self):
        patient = {
            'first_name': 'Bob',
            'last_name': 'Smith',
            'dob': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'bob.smithexample.com',
            'gender': 'Male'
        }

        response = self.client.post(self.url, patient, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_patient_missing_field(self):
        patient = {
            'last_name': 'Smith',
            'dob': '1990-01-01',
            'phone_number': '12345678901234567890',
            'email': 'bob.smith@example.com',
        }

        response = self.client.post(self.url, patient, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['first_name'], ['This field is required.'])
        self.assertEqual(response.data['gender'], ['This field is required.'])

    def test_create_patients_with_same_email(self):
        patient = {
            'first_name': 'Bob',
            'last_name': 'Smith',
            'dob': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'bob.smith@example.com',
            'gender': 'Male'
        }

        response = self.client.post(self.url, patient, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.url, patient, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field must be unique.', response.data['email'])

    def test_create_patient_with_invalid_dob(self):
        patient = {
            'first_name': 'Bob',
            'last_name': 'Smith',
            'dob': '1990-01-32',
            'phone_number': '1234567890',
            'email': 'bob.smith@example.com',
            'gender': 'Male'
        }

        response = self.client.post(self.url, patient, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Date has wrong format. Use one of these formats instead: YYYY-MM-DD.', response.data['dob'])
    
    def test_get_patients(self):
        patient = {
            'first_name': 'Bob',
            'last_name': 'Smith',
            'dob': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'bob.smith@example.com',
            'gender': 'Male'
        }

        response = self.client.post(self.url, patient, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], patient['first_name'].upper())
        self.assertEqual(response.data[0]['last_name'], patient['last_name'].upper())
        self.assertEqual(response.data[0]['dob'], patient['dob'])
        self.assertEqual(response.data[0]['phone_number'], patient['phone_number'])
        self.assertEqual(response.data[0]['email'], patient['email'].lower())
        self.assertEqual(response.data[0]['gender'], patient['gender'].upper())

    def test_delete_patient(self):
        patient = {
            'first_name': 'Bob',
            'last_name': 'Smith',
            'dob': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'bob.smith@example.com',
            'gender': 'Male'
        }

        response = self.client.post(self.url, patient, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        patient_id = response.data['id']
        response = self.client.delete(self.url + str(patient_id) + '/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_update_patient(self):
        patient = {
            'first_name': 'Bob',
            'last_name': 'Smith',
            'dob': '1990-01-01',
            'phone_number': '1234567890',
            'email': 'bob.smith@example.com',
            'gender': 'Male'
        }

        response = self.client.post(self.url, patient, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        patient_id = response.data['id']
        patient['first_name'] = 'Bob2'
        response = self.client.put(self.url + str(patient_id) + '/', patient, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], patient['first_name'].upper())

        patient_db = Patient.objects.get(id=patient_id)
        self.assertEqual(patient_db.first_name, patient['first_name'].upper())