from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import json
from datetime import timedelta
from django.conf import settings


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
        self.assertFalse(user.is_active)
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertFalse(user.subscribed)

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
        self.assertFalse(user.is_active)
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.company_name, '')
        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertFalse(user.subscribed)

    def test_create_jwt_token_fails_if_user_not_activated_after_signup(self):
        """
        Test that create jwt token view fails if user is not activated after
        signup.
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
        self.assertFalse(user.is_active)
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.company_name, '')
        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertFalse(user.subscribed)
        res = self.client.post(
            '/auth/jwt/create/',
            {
                'email': data['email'],
                'password': data['password'],
            }
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.data['detail'], 'No active account found with the given credentials')

    def test_signup_with_yes_credits_yes_subscription_leads_to_no_credits_no_subscription(self):
        """
        Test that attempting to singup with credits or subscription
        still leads to no credits and no subscription.
        """
        data = {
            'email': 'test@test.com',
            'password': 'testpass123',
            're_password': 'testpass123',
            'first_name': 'John',
            'last_name': 'Doe',
            'scats_credit': 999,
            'seasonality_credit': 999,
            'subscribed': True
        }
        res = self.client.post(
            '/auth/users/',
            data
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        user = get_user_model().objects.all()[0]
        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertFalse(user.subscribed)

    def test_retrieve_user_information_via_user_detail_view_fails(self):
        """
        Test that user cannot retrieve user information if he/she is
        not logged in.
        """
        res = self.client.get(reverse('users:user-detail'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_information_via_user_detail_view_fails(self):
        """
        Test that user cannot update user information if he/she is
        not logged in.
        """
        res = self.client.patch(
            reverse('users:user-detail'),
            {
                'first_name': 'Peter',
                'last_name': 'Parker'
            }
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

@override_settings(FREE_PERIOD_AFTER_ACCOUNT_CREATION = timedelta(days=2))
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

    def test_auth_users_view_returns_data_for_the_user_only(self):
        """
        Test that /auth/users/ view returns data for the user only.
        There should be no information about other users.
        """
        data = {
            'email': 'test2@test.com',
            'password': 'testpass123',
            're_password': 'testpass123',
            'first_name': 'Peter',
            'last_name': 'Smith',
        }
        res = self.client.post(
            '/auth/users/',
            data
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.all().count(), 2)

        res = self.client.get('/auth/users/')
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['first_name'], 'John')
        self.assertNotIn('Peter', json.dumps(res.data))

    def test_auth_users_view_does_not_return_unrequired_fields(self):
        """
        Test that /auth/users/ view does not return unrequired fields
        such as scats_credit, seasonality_credit, subscribed, and password
        """
        res = self.client.get('/auth/users/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_string = json.dumps(res.data)
        self.assertIn("first_name", res_string)
        self.assertIn("last_name", res_string)
        self.assertIn("company_name", res_string)
        self.assertIn("email", res_string)
        self.assertNotIn("scats_credit", res_string)
        self.assertNotIn("seasonality_credit", res_string)
        self.assertNotIn("subscribed", res_string)
        self.assertNotIn("password", res_string)

    def test_auth_users_me_view_does_not_return_unrequired_fields(self):
        """
        Test that /auth/users/me/ view does not return unrequired fields
        such as scats_credit, seasonality_credit, subscribed, and password
        """
        res = self.client.get('/auth/users/me/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_string = json.dumps(res.data)
        self.assertIn("first_name", res_string)
        self.assertIn("last_name", res_string)
        self.assertIn("company_name", res_string)
        self.assertIn("email", res_string)
        self.assertNotIn("scats_credit", res_string)
        self.assertNotIn("seasonality_credit", res_string)
        self.assertNotIn("subscribed", res_string)
        self.assertNotIn("password", res_string)

    def test_attempt_to_update_user_credits_and_subscription_info_via_patch_request_to_auth_users_me_view_leads_to_no_update(self):
        """
        Test that attempt to update user's credits and subscription
        information via patch request to /auth/users/me/ leads to no change.
        user.REQUIRED_FIELDS e.g. first_name, last_name, and company_name
        can still be updated.
        """
        user = get_user_model().objects.all()[0]
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.company_name, '3DP')
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertFalse(user.subscribed)

        res = self.client.patch(
            '/auth/users/me/',
            {
                'first_name': 'Peter',
                'last_name': 'Smith',
                'company_name': 'Microsoft',
                'email': 'whatever@whatever.com',
                'scats_credit': 999,
                'seasonality_credit': 999,
                'subscribed': True
            }
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        user = get_user_model().objects.all()[0]

        self.assertEqual(user.first_name, 'Peter')
        self.assertEqual(user.last_name, 'Smith'),
        self.assertEqual(user.company_name, 'Microsoft')
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertFalse(user.subscribed)

    def test_attempt_to_update_user_credits_and_subscription_info_via_put_request_to_auth_users_me_view_leads_to_no_update(self):
        """
        Test that attempt to update user's credits and subscription
        information via put request to /auth/users/me/ leads to no change.
        user.REQUIRED_FIELDS e.g. first_name, last_name, and company_name
        can still be updated.
        """
        user = get_user_model().objects.all()[0]
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.company_name, '3DP')
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertFalse(user.subscribed)

        res = self.client.put(
            '/auth/users/me/',
            {
                'first_name': 'Peter',
                'last_name': 'Smith',
                'company_name': 'Microsoft',
                'email': 'whatever@whatever.com',
                'scats_credit': 999,
                'seasonality_credit': 999,
                'subscribed': True
            }
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        user = get_user_model().objects.all()[0]

        self.assertEqual(user.first_name, 'Peter')
        self.assertEqual(user.last_name, 'Smith'),
        self.assertEqual(user.company_name, 'Microsoft')
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertFalse(user.subscribed)

    def test_retrieve_user_information_via_user_detail_view_successful(self):
        """
        Test that user can retrieve user information.
        """
        res = self.client.get(reverse('users:user-detail'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['first_name'], 'John')
        self.assertEqual(res.data['email'], 'test@test.com')
        self.assertEqual(res.data['scats_credit'], 0)
        self.assertEqual(res.data['seasonality_credit'], 0)
        self.assertFalse(res.data['subscribed'])
        self.assertIn('id', res.data)
        self.assertIn('email', res.data)
        self.assertIn('first_name', res.data)
        self.assertIn('last_name', res.data)
        self.assertIn('company_name', res.data)
        self.assertIn('scats_credit', res.data)
        self.assertIn('seasonality_credit', res.data)
        self.assertIn('subscribed', res.data)
        self.assertIn('free_until', res.data)
        self.assertNotIn('password', res.data)
        self.assertNotIn('subscription', res.data)

    def test_user_detail_view_returns_data_for_the_user_only(self):
        """
        Test that user detail view returns data for the user only.
        There should be no information about other users.
        """
        data = {
            'email': 'test2@test.com',
            'password': 'testpass123',
            're_password': 'testpass123',
            'first_name': 'Peter',
            'last_name': 'Smith',
        }
        res = self.client.post(
            '/auth/users/',
            data
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.all().count(), 2)

        res = self.client.get(reverse('users:user-detail'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(res.data, dict)
        self.assertEqual(res.data['email'], 'test@test.com')
        self.assertEqual(res.data['first_name'], 'John')
        self.assertNotEqual(res.data['email'], data['email'])
        self.assertNotEqual(res.data['first_name'], data['first_name'])

    def test_update_user_first_name_via_user_detail_view_sucessful(self):
        """
        Test that user can update first_name successfully.
        """
        data = {
            'first_name': 'Peter'
        }
        res = self.client.patch(reverse('users:user-detail'), data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        user = get_user_model().objects.all()[0]
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.company_name, '3DP')

        self.assertEqual(res.data['first_name'], data['first_name'])
        self.assertIn('id', res.data)
        self.assertIn('email', res.data)
        self.assertIn('first_name', res.data)
        self.assertIn('last_name', res.data)
        self.assertIn('company_name', res.data)
        self.assertIn('scats_credit', res.data)
        self.assertIn('seasonality_credit', res.data)
        self.assertIn('subscribed', res.data)
        self.assertIn('free_until', res.data)
        self.assertNotIn('password', res.data)
        self.assertNotIn('subscription', res.data)

    def test_update_user_last_name_via_user_detail_view_successful(self):
        """
        Test that user can update last_name successfully.
        """
        data = {
            'last_name': 'Parker'
        }
        res = self.client.patch(reverse('users:user-detail'), data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        user = get_user_model().objects.all()[0]
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.company_name, '3DP')

        self.assertEqual(res.data['last_name'], data['last_name'])
        self.assertIn('id', res.data)
        self.assertIn('email', res.data)
        self.assertIn('first_name', res.data)
        self.assertIn('last_name', res.data)
        self.assertIn('company_name', res.data)
        self.assertIn('scats_credit', res.data)
        self.assertIn('seasonality_credit', res.data)
        self.assertIn('subscribed', res.data)
        self.assertIn('free_until', res.data)
        self.assertNotIn('password', res.data)
        self.assertNotIn('subscription', res.data)

    def test_update_user_company_name_via_user_detail_view_successful(self):
        """
        Test that user can update company_name successfully.
        """
        data = {
            'company_name': 'Microsoft'
        }
        res = self.client.patch(reverse('users:user-detail'), data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        user = get_user_model().objects.all()[0]
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.company_name, data['company_name'])

        self.assertEqual(res.data['company_name'], data['company_name'])
        self.assertIn('id', res.data)
        self.assertIn('email', res.data)
        self.assertIn('first_name', res.data)
        self.assertIn('last_name', res.data)
        self.assertIn('company_name', res.data)
        self.assertIn('scats_credit', res.data)
        self.assertIn('seasonality_credit', res.data)
        self.assertIn('subscribed', res.data)
        self.assertIn('free_until', res.data)
        self.assertNotIn('password', res.data)
        self.assertNotIn('subscription', res.data)

    def test_update_user_email_via_user_detail_view_leads_to_no_change(self):
        """
        Test that user cannot update email.
        """
        data = {
            'email': 'email@email.com'
        }
        res = self.client.patch(reverse('users:user-detail'), data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        user = get_user_model().objects.all()[0]
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.company_name, '3DP')

        self.assertEqual(res.data['email'], 'test@test.com')
        self.assertIn('id', res.data)
        self.assertIn('email', res.data)
        self.assertIn('first_name', res.data)
        self.assertIn('last_name', res.data)
        self.assertIn('company_name', res.data)
        self.assertIn('scats_credit', res.data)
        self.assertIn('seasonality_credit', res.data)
        self.assertIn('subscribed', res.data)
        self.assertIn('free_until', res.data)
        self.assertNotIn('password', res.data)
        self.assertNotIn('subscription', res.data)

    def test_update_user_password_via_user_detail_view_leads_to_no_change(self):
        """
        Test that user cannot update password.
        """
        data = {
            'password': 'changedpassword123'
        }
        res = self.client.patch(reverse('users:user-detail'), data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        user = get_user_model().objects.all()[0]
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.company_name, '3DP')

        self.assertFalse(user.check_password(data['password']))
        self.assertTrue(user.check_password('testpass123'))

        self.assertIn('id', res.data)
        self.assertIn('email', res.data)
        self.assertIn('first_name', res.data)
        self.assertIn('last_name', res.data)
        self.assertIn('company_name', res.data)
        self.assertIn('scats_credit', res.data)
        self.assertIn('seasonality_credit', res.data)
        self.assertIn('subscribed', res.data)
        self.assertIn('free_until', res.data)
        self.assertNotIn('password', res.data)
        self.assertNotIn('subscription', res.data)

    def test_update_user_id_via_user_detail_view_leads_to_no_change(self):
        """
        Test that user cannot update id.
        """
        current_id = self.user.id
        data = {
            'id': current_id*3+1
        }
        res = self.client.patch(reverse('users:user-detail'), data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        user = get_user_model().objects.all()[0]
        self.assertEqual(user.id, current_id)
        self.assertNotEqual(user.id, data['id'])
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.company_name, '3DP')

        self.assertEqual(res.data['id'], current_id)
        self.assertNotEqual(res.data['id'], data['id'])
        self.assertIn('id', res.data)
        self.assertIn('email', res.data)
        self.assertIn('first_name', res.data)
        self.assertIn('last_name', res.data)
        self.assertIn('company_name', res.data)
        self.assertIn('scats_credit', res.data)
        self.assertIn('seasonality_credit', res.data)
        self.assertIn('subscribed', res.data)
        self.assertIn('free_until', res.data)
        self.assertNotIn('password', res.data)
        self.assertNotIn('subscription', res.data)

    def test_update_user_scats_credit_via_user_detail_view_leads_to_no_change(self):
        """
        Test that user cannot update scats_credit.
        """
        data = {
            'scats_credit': 999
        }
        res = self.client.patch(reverse('users:user-detail'), data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        user = get_user_model().objects.all()[0]
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.company_name, '3DP')
        self.assertEqual(user.scats_credit, 0)

        self.assertEqual(res.data['scats_credit'], 0)
        self.assertIn('id', res.data)
        self.assertIn('email', res.data)
        self.assertIn('first_name', res.data)
        self.assertIn('last_name', res.data)
        self.assertIn('company_name', res.data)
        self.assertIn('scats_credit', res.data)
        self.assertIn('seasonality_credit', res.data)
        self.assertIn('subscribed', res.data)
        self.assertIn('free_until', res.data)
        self.assertNotIn('password', res.data)
        self.assertNotIn('subscription', res.data)

    def test_update_user_seasonality_credit_via_user_detail_view_leads_to_no_change(self):
        """
        Test that user cannot update seasonality_credit.
        """
        data = {
            'seasonality_credit': 999
        }
        res = self.client.patch(reverse('users:user-detail'), data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        user = get_user_model().objects.all()[0]
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.company_name, '3DP')
        self.assertEqual(user.seasonality_credit, 0)

        self.assertEqual(res.data['seasonality_credit'], 0)
        self.assertIn('id', res.data)
        self.assertIn('email', res.data)
        self.assertIn('first_name', res.data)
        self.assertIn('last_name', res.data)
        self.assertIn('company_name', res.data)
        self.assertIn('scats_credit', res.data)
        self.assertIn('seasonality_credit', res.data)
        self.assertIn('subscribed', res.data)
        self.assertIn('free_until', res.data)
        self.assertNotIn('password', res.data)
        self.assertNotIn('subscription', res.data)

    def test_update_user_subscribed_via_user_detail_view_leads_to_no_change(self):
        """
        Test that user cannot update subscribed.
        """
        data = {
            'subscribed': True
        }
        res = self.client.patch(reverse('users:user-detail'), data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        user = get_user_model().objects.all()[0]
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.company_name, '3DP')
        self.assertFalse(user.subscribed)

        self.assertFalse(res.data['subscribed'])
        self.assertIn('id', res.data)
        self.assertIn('email', res.data)
        self.assertIn('first_name', res.data)
        self.assertIn('last_name', res.data)
        self.assertIn('company_name', res.data)
        self.assertIn('scats_credit', res.data)
        self.assertIn('seasonality_credit', res.data)
        self.assertIn('subscribed', res.data)
        self.assertIn('free_until', res.data)
        self.assertNotIn('password', res.data)
        self.assertNotIn('subscription', res.data)

    def test_update_user_free_until_via_user_detail_view_leads_to_no_change(self):
        """
        Test that user cannot update free_until.
        """
        current_free_until = self.user.free_until
        data = {
            'free_until': current_free_until + timedelta(weeks=7)
        }
        res = self.client.patch(reverse('users:user-detail'), data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        user = get_user_model().objects.all()[0]
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.company_name, '3DP')
        self.assertEqual(user.free_until, current_free_until)
        self.assertNotEqual(user.free_until, data['free_until'])

        self.assertEqual(res.data['free_until'], current_free_until)
        self.assertNotEqual(res.data['free_until'], data['free_until'])
        self.assertIn('id', res.data)
        self.assertIn('email', res.data)
        self.assertIn('first_name', res.data)
        self.assertIn('last_name', res.data)
        self.assertIn('company_name', res.data)
        self.assertIn('scats_credit', res.data)
        self.assertIn('seasonality_credit', res.data)
        self.assertIn('subscribed', res.data)
        self.assertIn('free_until', res.data)
        self.assertNotIn('password', res.data)
        self.assertNotIn('subscription', res.data)

    def test_newly_created_user_free_until_is_date_joined_plus_free_period_after_account_creation(self):
        """
        Test that newly created user's free_until is date_joined +
        settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION
        """
        data = {
            'email': 'newuser@test.com',
            'password': 'testpass123',
            're_password': 'testpass123',
            'first_name': 'Peter',
            'last_name': 'Parker',
            'company_name': 'Microsoft'
        }
        res = self.client.post(
            '/auth/users/',
            data
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(id=res.data['id'])

        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.free_until, user.date_joined+settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION)
