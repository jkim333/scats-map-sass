from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient


class PublicUsersApiTests(TestCase):
    """Test the publicly available users API"""
    def setUp(self):
        self.client = APIClient()
    
    def test_signup_successful_with_valid_inputs(self):
        """
        Test that signup is successful when valid inputs are provided.
        """
        data = {
            'email': 'test@test.com',
            'password': 'testpass123',
            're_password': 'testpass123',
            'first_name': 'John',
            'last_name': 'Doe',
            'company_name': '3DP'
        }
        res = self.client.post(
            '/auth/users/',
            data
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        user = get_user_model().objects.all()[0]
        self.assertEqual(user.email, data['email'])

    def test_signup_fails_if_email_not_provided(self):
        """
        Test that signup fails if email is not provided.
        """
        data = {
            'password': 'testpass123',
            're_password': 'testpass123',
            'first_name': 'John',
            'last_name': 'Doe',
            'company_name': '3DP'
        }
        res = self.client.post(
            '/auth/users/',
            data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.all().count(), 0)

    def test_signup_fails_if_first_name_not_provided(self):
        """
        Test that signup fails if first name is not provided.
        """
        data = {
            'email': 'test@test.com',
            'password': 'testpass123',
            're_password': 'testpass123',
            'last_name': 'Doe',
            'company_name': '3DP'
        }
        res = self.client.post(
            '/auth/users/',
            data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.all().count(), 0)

    def test_signup_fails_if_last_name_not_provided(self):
        """
        Test that signup fails if last name is not provided.
        """
        data = {
            'email': 'test@test.com',
            'password': 'testpass123',
            're_password': 'testpass123',
            'first_name': 'John',
            'company_name': '3DP'
        }
        res = self.client.post(
            '/auth/users/',
            data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.all().count(), 0)

    def test_signup_successful_without_company_name_provided(self):
        """
        Test that signup is successful even if company name is not provided.
        """
        data = {
            'email': 'test@test.com',
            'password': 'testpass123',
            're_password': 'testpass123',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        res = self.client.post(
            '/auth/users/',
            data
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        user = get_user_model().objects.all()[0]
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.company_name, '')

    def test_new_user_begins_with_zero_credit(self):
        """
        Test that a new user begins with zero credit.
        """
        data = {
            'email': 'test@test.com',
            'password': 'testpass123',
            're_password': 'testpass123',
            'first_name': 'John',
            'last_name': 'Doe',
            'company_name': '3DP'
        }
        res = self.client.post(
            '/auth/users/',
            data
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.all()[0]
        self.assertEqual(user.credit, 0)


class PrivateUsersApiTests(TestCase):
    """Test the private users API"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP'
        )
        self.client.force_authenticate(user=self.user)
