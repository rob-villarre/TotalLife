from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from rest_framework.exceptions import ValidationError

from .models import Clinician

class CliniciansAPITests(APITestCase):
    def setUp(self):
        self.url = '/api/clinicians/'
        self.clinician = {
            'first_name': 'BOB',
            'last_name': 'SMITH',
            'npi_number': '1234567890',
            'state': 'CA'
        }
        return super().setUp()
    
    # mock validate method that uses external API to validate NPI number
    @patch('clinicians.serializer.ClinicianSerializer.validate')
    def test_create_clinician(self, mock_validate):
        mock_validate.return_value = self.clinician
        response = self.client.post(self.url, self.clinician, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_validate.assert_called_once_with(self.clinician)
        self.assertEqual(response.data['first_name'], self.clinician['first_name'])
        self.assertEqual(response.data['last_name'], self.clinician['last_name'])
        self.assertEqual(response.data['npi_number'], self.clinician['npi_number'])
        self.assertEqual(response.data['state'], self.clinician['state'])

    @patch('clinicians.serializer.ClinicianSerializer.validate')
    def test_create_clinician_invalid_npi_number(self, mock_validate):
        mock_validate.side_effect = ValidationError({"npi_number": ["Invalid NPI number."]})
        response = self.client.post(self.url, self.clinician, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['npi_number'], ['Invalid NPI number.'])

    def test_create_clinician_missing_field(self):
        clinician = {
            'first_name': 'Bob',
            'last_name': 'Smith',
            'npi_number': '1234567890',
        }

        response = self.client.post(self.url, clinician, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['state'], ['This field is required.'])

    @patch('clinicians.serializer.ClinicianSerializer.validate')
    def test_create_clinician_with_same_npi_number(self, mock_validate):
        mock_validate.return_value = self.clinician

        response = self.client.post(self.url, self.clinician, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.url, self.clinician, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field must be unique.', response.data['npi_number'])

    @patch('clinicians.serializer.ClinicianSerializer.validate')
    def test_get_clinicians(self, mock_validate):
        mock_validate.return_value = self.clinician
        response = self.client.post(self.url, self.clinician, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], self.clinician['first_name'])
        self.assertEqual(response.data[0]['last_name'], self.clinician['last_name'])
        self.assertEqual(response.data[0]['npi_number'], self.clinician['npi_number'])
        self.assertEqual(response.data[0]['state'], self.clinician['state'])

    @patch('clinicians.serializer.ClinicianSerializer.validate')
    def test_get_clinician(self, mock_validate):
        mock_validate.return_value = self.clinician
        response = self.client.post(self.url, self.clinician, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        clinician_id = response.data['id']
        response = self.client.get(self.url + str(clinician_id) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.clinician['first_name'])
        self.assertEqual(response.data['last_name'], self.clinician['last_name'])
        self.assertEqual(response.data['npi_number'], self.clinician['npi_number'])
        self.assertEqual(response.data['state'], self.clinician['state'])

    @patch('clinicians.serializer.ClinicianSerializer.validate')
    def test_delete_clinician(self, mock_validate):
        mock_validate.return_value = self.clinician
        response = self.client.post(self.url, self.clinician, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        clinician_id = response.data['id']
        response = self.client.delete(self.url + str(clinician_id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    @patch('clinicians.serializer.ClinicianSerializer.validate')
    def test_update_clinician(self, mock_validate):
        mock_validate.return_value = self.clinician
        response = self.client.post(self.url, self.clinician, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        clinician_id = response.data['id']
        self.clinician['first_name'] = 'BOB2'
        response = self.client.put(self.url + str(clinician_id) + '/', self.clinician, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.clinician['first_name'])

        clinician_db = Clinician.objects.get(id=clinician_id)
        self.assertEqual(clinician_db.first_name, self.clinician['first_name'])