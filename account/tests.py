"""External Import"""
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase

"""Internal Import"""
from master.utils import PasswordRecover

class StudentAPITests(APITestCase):
    def setUp(self):
        login_url = reverse('login')

        user_data = {
            'username': 'sky2aa',
            'password': 'Ab3456'
        }
        response = self.client.post(login_url, user_data)
        self.token = response.data.get('access_token')
        self.assertIsNotNone(self.token, "Token is required for authenticated requests")

    def test_create_student(self):
        """
        Test creating a new student.
        """
        url = reverse('create-student')
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            'name': 'Test Student',
            'subject_id': 1,
            'mark': 95
        }

        response = self.client.post(url, data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_student(self):
        """
        Test editing an existing student's details.
        """
        student = {
            'name': 'Existing Student',
            'subject_id': 1,
            'mark': 80
        }
        create_url = reverse('create-student')
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = self.client.post(create_url, student, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        student_id = response.data['id']
        edit_url = reverse('edit-student', args=[student_id])

        update_data = {
            'name': 'Updated Student Name',
            'subject_id': 1,
            'mark': 90
        }

        response = self.client.put(edit_url, update_data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_student(self):
        """
        Test deleting an existing student.
        """
        student = {
            'name': 'Student to Delete',
            'subject_id': 1,
            'mark': 85
        }
        create_url = reverse('create-student')
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = self.client.post(create_url, student, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        student_id = response.data['id']
        delete_url = reverse('delete-student', args=[student_id])

        response = self.client.delete(delete_url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_student_not_found_for_edit(self):
        """
        Test editing a student that doesn't exist.
        """
        url = reverse('edit-student', args=[999])
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        update_data = {
            'name': 'Non Existing Student',
            'subject_id': 1,
            'mark': 75
        }
        response = self.client.put(url, update_data, headers=headers)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subject_not_found_for_create(self):
        """
        Test creating a student with an invalid subject.
        """
        url = reverse('create-student')
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            'name': 'Student with Invalid Subject',
            'subject_id': 999,
            'mark': 85
        }
        response = self.client.post(url, data, headers=headers)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "Invalid subject ID") 

    def test_password_obscure(self):
        """
        Test obscuring the password.
        """
        password = 'password123'
        obscured_password = PasswordRecover.obscure_password(password)
        
        self.assertEqual(obscured_password, 'pa******23')
