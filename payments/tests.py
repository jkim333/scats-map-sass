from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.conf import settings
from unittest.mock import Mock, patch


class PublicPaymentsApiTests(TestCase):
    """Test the publicly available payments API"""

    def setUp(self):
        self.client = APIClient()

    def test_access_create_checkout_session_view_fails(self):
        """
        Test that access to Create Checkout Session view fails.
        """
        res = self.client.post(reverse('payments:create-checkout-session'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_get_subscription_info_view_fails(self):
        """
        Test that access to Get Subscription Info view fails.
        """
        res = self.client.get(reverse('payments:get-subscription-info'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_cancel_subscription_view_fails(self):
        """
        Test that access to Cancel Subscription View fails.
        """
        res = self.client.post(reverse('payments:cancel-subscription'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_reactivate_cancelled_subscription_view_fails(self):
        """
        Test that access to reactivate Cancelled Subscription View fails.
        """
        res = self.client.post(reverse('payments:reactivate-cancelled-subscription'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePaymentsApiCreateCheckoutSessionTests(TestCase):
    """Test the private payments API for CreateCheckoutSession view"""

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

    @patch('payments.views.stripe.checkout.Session')
    def test_create_checkout_session_order_scats_credit_only_successful(self, mock_checkout_session):
        """
        Test that user can successfully create checkout session for ordering
        Scats Credit only.
        """
        mock_checkout_session.create.return_value.url = 'some_url'

        data = {
            "orders": [
                {
                    "price_id": settings.STRIPE_SCATS_CREDIT_PRICE_ID,
                    "quantity": 5
                }
            ]
        }
        res = self.client.post(
            reverse('payments:create-checkout-session'),
            data,
            format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('checkout_url', res.data)
        self.assertEqual(res.data['checkout_url'], 'some_url')

    @patch('payments.views.stripe.checkout.Session')
    def test_create_checkout_session_order_seasonality_credit_only_successful(self, mock_checkout_session):
        """
        Test that user can successfully create checkout session for ordering
        Seasonality Credit only.
        """
        mock_checkout_session.create.return_value.url = 'some_url'

        data = {
            "orders": [
                {
                    "price_id": settings.STRIPE_SEASONALITY_CREDIT_PRICE_ID,
                    "quantity": 5
                }
            ]
        }
        res = self.client.post(
            reverse('payments:create-checkout-session'),
            data,
            format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('checkout_url', res.data)
        self.assertEqual(res.data['checkout_url'], 'some_url')

    @patch('payments.views.stripe.checkout.Session')
    def test_create_checkout_session_order_scats_and_seasonality_credits_successful(self, mock_checkout_session):
        """
        Test that user can successfully create checkout session for ordering
        both Scats and Seasonality Credit.
        """
        mock_checkout_session.create.return_value.url = 'some_url'

        data = {
            "orders": [
                {
                    "price_id": settings.STRIPE_SCATS_CREDIT_PRICE_ID,
                    "quantity": 5
                },
                {
                    "price_id": settings.STRIPE_SEASONALITY_CREDIT_PRICE_ID,
                    "quantity": 5
                }
            ]
        }
        res = self.client.post(
            reverse('payments:create-checkout-session'),
            data,
            format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('checkout_url', res.data)
        self.assertEqual(res.data['checkout_url'], 'some_url')

    @patch('payments.views.stripe.checkout.Session')
    def test_create_checkout_session_order_nothing_fails(self, mock_checkout_session):
        """
        Test that creating checkout session with no order items fail.
        """
        mock_checkout_session.create.return_value.url = 'some_url'

        data = {
            "orders": []
        }
        res = self.client.post(
            reverse('payments:create-checkout-session'),
            data,
            format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'Your order cannot be empty.')

    def test_create_checkout_session_with_invalid_price_id_fails(self):
        """
        Test that creating checkout session with invalid price_id fails.
        """
        data = {
            "orders": [
                {
                    "price_id": 'random_price_id',
                    "quantity": 5
                },
            ]
        }
        res = self.client.post(
            reverse('payments:create-checkout-session'),
            data,
            format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No such price: 'random_price_id'", res.data['error'])

    def test_create_checkout_session_with_quantity_less_than_or_equal_to_zero_fails(self):
        """
        Test that creating checkout session with quantity less than or
        equal to 0 fails.
        """
        data = {
            "orders": [
                {
                    "price_id": settings.STRIPE_SCATS_CREDIT_PRICE_ID,
                    "quantity": 5
                },
                {
                    "price_id": settings.STRIPE_SEASONALITY_CREDIT_PRICE_ID,
                    "quantity": 0
                }
            ]
        }
        res = self.client.post(
            reverse('payments:create-checkout-session'),
            data,
            format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'This value must be greater than or equal to 1',
            res.data['error']
        )

    @patch('payments.views.stripe.checkout.Session')
    def test_create_checkout_session_order_subscription_successful(self, mock_checkout_session):
        """
        Test that user can successfully create checkout session for ordering
        subscription.
        """
        mock_checkout_session.create.return_value.url = 'some_url'

        data = {
            "subscription": True
        }
        res = self.client.post(
            reverse('payments:create-checkout-session'),
            data,
            format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('checkout_url', res.data)
        self.assertEqual(res.data['checkout_url'], 'some_url')

    def test_create_checkout_session_subscription_false_fails(self):
        """
        Test that creating checkout session for subscription with
        subscription=False fails.
        """
        data = {
            "subscription": False
        }
        res = self.client.post(
            reverse('payments:create-checkout-session'),
            data,
            format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', res.data)

    def test_create_checkout_session_empty_data_fails(self):
        """
        Test that creating checkout session with empty data fails.
        """
        data = {}
        res = self.client.post(
            reverse('payments:create-checkout-session'),
            data,
            format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', res.data)

    def test_user_cannot_double_subscribe(self):
        """
        Test that user cannot double subscribe.
        """
        self.user.subscribed = True
        self.user.save()

        data = {
            "subscription": True
        }
        res = self.client.post(
            reverse('payments:create-checkout-session'),
            data,
            format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], 'You are already on a subscription.')
