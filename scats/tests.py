from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from _tools.add_to_db import add_to_db
import json
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
from django.conf import settings


class PublicScatsApiTests(TestCase):
    """Test the publicly available scats API"""
    def setUp(self):
        self.client = APIClient()
    
    def test_access_to_opsheet_download_view_fails(self):
        """
        Test that access to opsheet download view fails.
        """
        res = self.client.get(
            reverse('scats:opsheet-download', kwargs={'scats_id': 100})
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_to_extract_scats_data_view_fails(self):
        """
        Test that access to extract scats data view fails.
        """
        res = self.client.get(
            reverse('scats:extract-scats-data')+'?scats_id=100&from=2021-06-10&to=2021-06-17'
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_to_seasonality_analysis_view_fails(self):
        """
        Test that access to seasonality analysis view fails.
        """
        res = self.client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-06-10&to=2022-06-09&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

@override_settings(QT_INTERVAL_COUNT_MIN=date(2000, 1, 1), QT_INTERVAL_COUNT_MAX=date(2030, 1, 1), FREE_PERIOD_AFTER_ACCOUNT_CREATION = timedelta(days=2))
class PrivateUsersApiTests(TestCase):
    """Test the private users API"""
    @classmethod
    def setUpTestData(cls):
        # create scats objects and build the db
        add_to_db(r'C:\Users\Jihyung\Desktop\scats_seasonality\backend\scats\test_data\input')

    def test_access_to_opsheet_download_view_with_no_scats_credit_no_seasonality_credit_no_subscription_succeeds(self):
        """
        Test that access to opsheet download view succeeds with
        no scats credit, no seasonality credit and no subscription.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP'
        )
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:opsheet-download', kwargs={'scats_id': 100})
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, 'url')

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

    def test_access_to_extract_scats_data_view_with_no_scats_credit_no_seasonality_credit_no_subscription_fails(self):
        """
        Test that access to extract scats data view fails with
        no scats credit, no seasonality credit and no subscription.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP'
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=100&from=2021-07-01&to=2021-07-05'
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['error'], 'Access denied. Please purchase scats credit points or sign up for the monthly subscription.')

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

    def test_access_to_extract_scats_data_view_with_no_scats_credit_yes_seasonality_credit_no_subscription_fails(self):
        """
        Test that access to extract scats data view fails with
        no scats credit, yes seasonality credit and no subscription.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            seasonality_credit=3,
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=100&from=2021-07-01&to=2021-07-05'
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['error'], 'Access denied. Please purchase scats credit points or sign up for the monthly subscription.')

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

    def test_access_to_extract_scats_data_view_with_no_scats_credit_no_seasonality_credit_yes_subscription_succeeds(self):
        """
        Test that access to extract scats data view succeeds with
        no scats credit, no seasonality credit and yes subscription.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            subscribed=True
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, True)

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=100&from=2021-07-01&to=2021-07-05'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_string = json.dumps(json.loads(res.content))
        self.assertIn('"NB_SCATS_SITE": 100', res_string)
        self.assertNotIn('"NB_SCATS_SITE": 101', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-01"', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-02"', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-03"', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-04"', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-05"', res_string)
        self.assertNotIn('"QT_INTERVAL_COUNT": "2021-07-06"', res_string)
        self.assertEqual(
            json.loads(res.content)[0]['QT_INTERVAL_COUNT'],
            '2021-07-01'
        )
        self.assertEqual(
            json.loads(res.content)[-1]['QT_INTERVAL_COUNT'],
            '2021-07-05'
        )

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, True)

    def test_access_to_extract_scats_data_view_with_yes_scats_credit_no_seasonality_credit_no_subscription_succeeds(self):
        """
        Test that access to extract scats data view succeeds with
        yes scats credit, no seasonality credit and no subscription.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=100&from=2021-07-01&to=2021-07-05'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_string = json.dumps(json.loads(res.content))
        self.assertIn('"NB_SCATS_SITE": 100', res_string)
        self.assertNotIn('"NB_SCATS_SITE": 101', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-01"', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-02"', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-03"', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-04"', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-05"', res_string)
        self.assertNotIn('"QT_INTERVAL_COUNT": "2021-07-06"', res_string)
        self.assertEqual(
            json.loads(res.content)[0]['QT_INTERVAL_COUNT'],
            '2021-07-01'
        )
        self.assertEqual(
            json.loads(res.content)[-1]['QT_INTERVAL_COUNT'],
            '2021-07-05'
        )

        self.assertEqual(user.scats_credit, 2)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

    def test_access_to_extract_scats_data_view_with_yes_scats_credit_yes_seasonality_credit_yes_subscription_does_not_deduct_any_credit(self):
        """
        Test that access to extract scats data view with
        yes scats credit, yes seasonality credit and yes subscription
        does not deduct any credit points.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
            seasonality_credit=3,
            subscribed=True
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, True)

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=100&from=2021-07-01&to=2021-07-05'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_string = json.dumps(json.loads(res.content))
        self.assertIn('"NB_SCATS_SITE": 100', res_string)
        self.assertNotIn('"NB_SCATS_SITE": 101', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-01"', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-02"', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-03"', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-04"', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-05"', res_string)
        self.assertNotIn('"QT_INTERVAL_COUNT": "2021-07-06"', res_string)
        self.assertEqual(
            json.loads(res.content)[0]['QT_INTERVAL_COUNT'],
            '2021-07-01'
        )
        self.assertEqual(
            json.loads(res.content)[-1]['QT_INTERVAL_COUNT'],
            '2021-07-05'
        )

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, True)

    def test_access_to_extract_scats_data_view_with_invalid_scats_id_fails(self):
        """
        Test that access to extract scats data view with invalid scats_id fails.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=invalid&from=2021-07-01&to=2021-07-05'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], "'scats_id' must be an integer.")

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

    def test_access_to_extract_scats_data_view_with_invalid_from_fails(self):
        """
        Test that access to extract scats data view with invalid from fails.
        +
        Test that from date is greater than the minimum database date.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=100&from=invalid&to=2021-07-05'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], "'from' must be a date of format YYYY-MM-DD.")

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=100&from=1990-01-01&to=2021-07-05'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], f"'from' must be a date later than or equal to {settings.QT_INTERVAL_COUNT_MIN}")

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

    def test_access_to_extract_scats_data_view_with_invalid_to_fails(self):
        """
        Test that access to extract scats data view with invalid to fails.
        +
        Test that to date is less than the maximum database date.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=100&from=2021-07-01&to=invalid'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], "'to' must be a date of format YYYY-MM-DD.")

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=100&from=2021-07-01&to=2050-01-01'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], f"'to' must be a date earlier than or equal to {settings.QT_INTERVAL_COUNT_MAX}")

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

    def test_access_to_extract_scats_data_view_with_difference_between_from_and_to_more_than_seven_days_fails(self):
        """
        Test that access to extract scats data view with the difference between
        from and to dates more than 7 days fails.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=100&from=2021-07-01&to=2021-07-08'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], "Time difference between 'from' and 'to' cannot be more than 7 days.")

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

    def test_access_to_extract_scats_data_view_with_from_greater_than_to_fails(self):
        """
        Test that access to extract scats data view with from date
        greater than to date fails.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=700&from=2021-07-03&to=2021-07-01'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], "'from' cannot be greater than 'to'.")

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

    def test_access_to_extract_scats_data_view_with_from_equal_to_to_succeeds(self):
        """
        Test that access to extract scats data view with from date
        equal to to date succeeds.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=100&from=2021-07-01&to=2021-07-01'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_string = json.dumps(json.loads(res.content))
        self.assertIn('"NB_SCATS_SITE": 100', res_string)
        self.assertNotIn('"NB_SCATS_SITE": 101', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-01"', res_string)
        self.assertNotIn('"QT_INTERVAL_COUNT": "2021-06-30"', res_string)
        self.assertNotIn('"QT_INTERVAL_COUNT": "2021-07-02"', res_string)
        self.assertEqual(
            json.loads(res.content)[0]['QT_INTERVAL_COUNT'],
            '2021-07-01'
        )
        self.assertEqual(
            json.loads(res.content)[-1]['QT_INTERVAL_COUNT'],
            '2021-07-01'
        )

        self.assertEqual(user.scats_credit, 2)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

    def test_access_to_extract_scats_data_view_fails_if_no_data_found(self):
        """
        Test that access to extract scats data view fails if there was no data
        found.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=700&from=2021-08-01&to=2021-08-05'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], "There was no data found. Please try again with a different request.")

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

    def test_extract_scats_data_view_returns_data_ordered_by_qt_interval_count_and_nb_detector(self):
        """
        Test that extract scats data view returns data that are ordered by QT_INTERVAL_COUNT and NB_DETECTOR in ascending order.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
            seasonality_credit=0,
            subscribed=False
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=100&from=2021-07-01&to=2021-07-05'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_json = json.loads(res.content)
        res_string = json.dumps(res_json)
        self.assertIn('"NB_SCATS_SITE": 100', res_string)
        self.assertNotIn('"NB_SCATS_SITE": 101', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-01"', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-02"', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-03"', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-04"', res_string)
        self.assertIn('"QT_INTERVAL_COUNT": "2021-07-05"', res_string)
        self.assertNotIn('"QT_INTERVAL_COUNT": "2021-07-06"', res_string)
        self.assertEqual(
            json.loads(res.content)[0]['QT_INTERVAL_COUNT'],
            '2021-07-01'
        )
        self.assertEqual(
            json.loads(res.content)[-1]['QT_INTERVAL_COUNT'],
            '2021-07-05'
        )

        prev_val = 0
        for data in res_json:
            i = datetime.strptime(data['QT_INTERVAL_COUNT'], "%Y-%m-%d").timestamp()
            i += data['NB_DETECTOR']
            self.assertGreater(i, prev_val)
            prev_val = i

        self.assertEqual(user.scats_credit, 2)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

    def test_extract_scats_data_view_successful_with_no_scats_credit_no_seasonality_credit_no_subscription_newly_created_account(self):
        """
        Test that extract scats data view is successful with no scats credit,
        no seasonality credit, no subscription when the account is newly created and is on the free period.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=0,
            seasonality_credit=0,
            subscribed=False
        )
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=100&from=2021-07-01&to=2021-07-05'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

    def test_extract_scats_data_view_successful_with_yes_scats_credit_yes_seasonality_credit_no_subscription_newly_created_account(self):
        """
        Test that extract scats data view is successful with scats credit,
        seasonality credit, no subscription when the account is newly created
        and is on the free period.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
            seasonality_credit=3,
            subscribed=False
        )
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=100&from=2021-07-01&to=2021-07-05'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

    def test_extract_scats_data_view_successful_with_yes_scats_credit_yes_seasonality_credit_yes_subscription_newly_created_account(self):
        """
        Test that extract scats data view is successful with scats credit,
        seasonality credit, subscription when the account is newly created and is on the free period.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
            seasonality_credit=3,
            subscribed=True
        )
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, True)

        res = client.get(
            reverse('scats:extract-scats-data')+'?scats_id=100&from=2021-07-01&to=2021-07-05'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, True)

    def test_access_to_seasonality_analysis_view_with_no_scats_credit_no_seasonality_credit_no_subscription_fails(self):
        """
        Test that access to seasonality analysis view fails with
        no scats credit, no seasonality credit and no subscription.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP'
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-01&to=2021-07-05&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['error'], 'Access denied. Please purchase seasonality analysis credit points or sign up for the monthly subscription.')

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

    def test_access_to_seasonality_analysis_view_with_no_scats_credit_yes_seasonality_credit_no_subscription_succeeds(self):
        """
        Test that access to seasonality analysis view succeeds with
        no scats credit, yes seasonality credit and no subscription.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            seasonality_credit=3
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-01&to=2021-07-05&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        validation_df = pd.read_csv(r'C:\Users\Jihyung\Desktop\scats_seasonality\backend\scats\test_data\validation.csv', index_col='QT_INTERVAL_COUNT').dropna(axis='index')
        validation_df.index = pd.to_datetime(validation_df.index)

        res_df = pd.io.json.read_json(json.dumps(res.data), orient='table')
        res_df.index = pd.to_datetime(res_df.index)
        res_df.index = res_df.index.tz_localize(None)

        self.assertAlmostEqual(np.absolute((validation_df - res_df).to_numpy()).sum(), 0, places=3)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 2)
        self.assertEqual(user.subscribed, False)

    def test_access_to_seasonality_analysis_view_with_no_scats_credit_no_seasonality_credit_yes_subscription_succeeds(self):
        """
        Test that access to seasonality analysis view succeeds with
        no scats credit, no seasonality credit and yes subscription.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            subscribed=True
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, True)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-01&to=2021-07-05&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        validation_df = pd.read_csv(r'C:\Users\Jihyung\Desktop\scats_seasonality\backend\scats\test_data\validation.csv', index_col='QT_INTERVAL_COUNT').dropna(axis='index')
        validation_df.index = pd.to_datetime(validation_df.index)

        res_df = pd.io.json.read_json(json.dumps(res.data), orient='table')
        res_df.index = pd.to_datetime(res_df.index)
        res_df.index = res_df.index.tz_localize(None)

        self.assertAlmostEqual(np.absolute((validation_df - res_df).to_numpy()).sum(), 0, places=3)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, True)

    def test_access_to_seasonality_analysis_view_with_yes_scats_credit_no_seasonality_credit_no_subscription_fails(self):
        """
        Test that access to seasonality analysis view fails with
        yes scats credit, no seasonality credit and no subscription.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-01&to=2021-07-05&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['error'], 'Access denied. Please purchase seasonality analysis credit points or sign up for the monthly subscription.')

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

    def test_access_to_seasonality_analysis_view_with_yes_scats_credit_yes_seasonality_credit_yes_subscription_does_not_deduct_any_credit(self):
        """
        Test that access to seasonality analysis view with
        yes scats credit, yes seasonality credit and yes subscription
        does not deduct any credit points.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
            seasonality_credit=3,
            subscribed=True
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, True)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-01&to=2021-07-05&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        validation_df = pd.read_csv(r'C:\Users\Jihyung\Desktop\scats_seasonality\backend\scats\test_data\validation.csv', index_col='QT_INTERVAL_COUNT').dropna(axis='index')
        validation_df.index = pd.to_datetime(validation_df.index)

        res_df = pd.io.json.read_json(json.dumps(res.data), orient='table')
        res_df.index = pd.to_datetime(res_df.index)
        res_df.index = res_df.index.tz_localize(None)

        self.assertAlmostEqual(np.absolute((validation_df - res_df).to_numpy()).sum(), 0, places=3)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, True)

    def test_access_to_seasonality_analysis_view_with_invalid_scats_id_fails(self):
        """
        Test that access to seasonality analysis view with invalid scats_id fails.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
            seasonality_credit=3
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=invalid&from=2021-07-01&to=2021-07-05&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], "'scats_id' must be an integer.")

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

    def test_access_to_seasonality_analysis_view_with_invalid_from_fails(self):
        """
        Test that access to seasonality analysis view with invalid from fails.
        +
        Test that from date is greater than the minimum database date.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            seasonality_credit=3,
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=invalid&to=2021-07-05&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], "'from' must be a date of format YYYY-MM-DD.")

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=1990-01-01&to=2021-07-05&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], f"'from' must be a date later than or equal to {settings.QT_INTERVAL_COUNT_MIN}")

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

    def test_access_to_seasonality_analysis_view_with_invalid_to_fails(self):
        """
        Test that access to seasonality analysis view with invalid to fails.
        +
        Test that to date is less than the maximum database date.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            seasonality_credit=3,
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-01&to=invalid&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], "'to' must be a date of format YYYY-MM-DD.")

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-01&to=2050-01-01&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], f"'to' must be a date earlier than or equal to {settings.QT_INTERVAL_COUNT_MAX}")

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

    def test_access_to_seasonality_analysis_view_with_difference_between_from_and_to_more_than_three_hundred_sixty_five_days_fails(self):
        """
        Test that access to seasonality analysis view with the difference between from and to dates more than 365 days fails.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
            seasonality_credit=3
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-01&to=2022-07-01&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], "Time difference between 'from' and 'date' cannot be more than 365 days.")

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

    def test_access_to_seasonality_analysis_view_with_from_greater_than_to_fails(self):
        """
        Test that access to seasonality analysis view with from date greater
        than to date fails.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
            seasonality_credit=3
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-05&to=2021-07-01&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], "'from' cannot be greater than 'to'.")

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

    def test_access_to_seasonality_analysis_view_with_from_equal_to_to_succeeds(self):
        """
        Test that access to seasonality analysis view with from date equal to
        to date succeeds.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
            seasonality_credit=3,
            subscribed=False
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-01&to=2021-07-01&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        validation_df = pd.read_csv(r'C:\Users\Jihyung\Desktop\scats_seasonality\backend\scats\test_data\validation_20210701.csv', index_col='QT_INTERVAL_COUNT').dropna(axis='index')
        validation_df.index = pd.to_datetime(validation_df.index)

        res_df = pd.io.json.read_json(json.dumps(res.data), orient='table')
        res_df.index = pd.to_datetime(res_df.index)
        res_df.index = res_df.index.tz_localize(None)

        self.assertAlmostEqual(np.absolute((validation_df - res_df).to_numpy()).sum(), 0, places=3)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 2)
        self.assertEqual(user.subscribed, False)

    def test_access_to_seasonality_analysis_view_with_invalid_detectors_fails(self):
        """
        Test that access to seasonality analysis view with invalid detectors fails.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
            seasonality_credit=3
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-01&to=2021-07-05&detectors=invalid'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], "'detectors' must be integers separated by comma.")

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

    def test_access_to_seasonality_analysis_view_with_detectors_all_or_none_produces_outputs_for_all_detectors(self):
        """
        Test that access to seasonality analysis view with detectors equal to
        'all' or None produces output for all detectors.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            seasonality_credit=3
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-01&to=2021-07-05&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        validation_df = pd.read_csv(r'C:\Users\Jihyung\Desktop\scats_seasonality\backend\scats\test_data\validation.csv', index_col='QT_INTERVAL_COUNT').dropna(axis='index')
        validation_df.index = pd.to_datetime(validation_df.index)

        res_df = pd.io.json.read_json(json.dumps(res.data), orient='table')
        res_df.index = pd.to_datetime(res_df.index)
        res_df.index = res_df.index.tz_localize(None)

        self.assertAlmostEqual(np.absolute((validation_df - res_df).to_numpy()).sum(), 0, places=3)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 2)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-01&to=2021-07-05&detectors='
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        validation_df = pd.read_csv(r'C:\Users\Jihyung\Desktop\scats_seasonality\backend\scats\test_data\validation.csv', index_col='QT_INTERVAL_COUNT').dropna(axis='index')
        validation_df.index = pd.to_datetime(validation_df.index)

        res_df = pd.io.json.read_json(json.dumps(res.data), orient='table')
        res_df.index = pd.to_datetime(res_df.index)
        res_df.index = res_df.index.tz_localize(None)

        self.assertAlmostEqual(np.absolute((validation_df - res_df).to_numpy()).sum(), 0, places=3)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 1)
        self.assertEqual(user.subscribed, False)

    def test_access_to_seasonality_analysis_view_with_specific_detectors_produces_outputs_for_specific_detectors(self):
        """
        Test that access to seasonality analysis view with specific detectors
        produces outputs for specific detectors.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            seasonality_credit=3
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-01&to=2021-07-05&detectors=1,2,3'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        validation_df = pd.read_csv(r'C:\Users\Jihyung\Desktop\scats_seasonality\backend\scats\test_data\validation_detectors_1_2_3.csv', index_col='QT_INTERVAL_COUNT').dropna(axis='index')
        validation_df.index = pd.to_datetime(validation_df.index)

        res_df = pd.io.json.read_json(json.dumps(res.data), orient='table')
        res_df.index = pd.to_datetime(res_df.index)
        res_df.index = res_df.index.tz_localize(None)

        self.assertAlmostEqual(np.absolute((validation_df - res_df).to_numpy()).sum(), 0, places=3)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 2)
        self.assertEqual(user.subscribed, False)

    def test_access_to_seasonality_analysis_view_fails_if_no_data_found(self):
        """
        Test that access to seasonality analysis view fails if there was no data
        found.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
            seasonality_credit=3
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-06&to=2021-07-08&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'], "There was no data found. Please try again with a different request.")

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

    def test_seasonality_analysis_view_returns_data_ordered_by_qt_interval_count(self):
        """
        Test that seasonality analysis view returns data that are ordered by QT_INTERVAL_COUNT in ascending order.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            seasonality_credit=3
        )
        # This step is necessary to make sure that
        # user is not on the free period after creating account.
        user.date_joined = user.date_joined - (settings.FREE_PERIOD_AFTER_ACCOUNT_CREATION + timedelta(minutes=1))
        user.save()
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-01&to=2021-07-05&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        validation_df = pd.read_csv(r'C:\Users\Jihyung\Desktop\scats_seasonality\backend\scats\test_data\validation.csv', index_col='QT_INTERVAL_COUNT').dropna(axis='index')
        validation_df.index = pd.to_datetime(validation_df.index)

        res_df = pd.io.json.read_json(json.dumps(res.data), orient='table')
        res_df.index = pd.to_datetime(res_df.index)
        res_df.index = res_df.index.tz_localize(None)

        self.assertAlmostEqual(np.absolute((validation_df - res_df).to_numpy()).sum(), 0, places=3)

        prev_val = 0
        for data in res.data['data']:
            i = datetime.strptime(data['QT_INTERVAL_COUNT'].split('T')[0], "%Y-%m-%d").timestamp()
            self.assertGreater(i, prev_val)
            prev_val = i

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 2)
        self.assertEqual(user.subscribed, False)

    def test_seasonality_analysis_view_successful_with_no_scats_credit_no_seasonality_credit_no_subscription_newly_created_account(self):
        """
        Test that seasonality analysis view is successful with no scats credit,
        no seasonality credit, no subscription when the account is newly created and is on the free period.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=0,
            seasonality_credit=0,
            subscribed=False
        )
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-01&to=2021-07-05&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(user.scats_credit, 0)
        self.assertEqual(user.seasonality_credit, 0)
        self.assertEqual(user.subscribed, False)

    def test_seasonality_analysis_view_successful_with_yes_scats_credit_yes_seasonality_credit_no_subscription_newly_created_account(self):
        """
        Test that seasonality analysis view is successful with scats credit,
        seasonality credit, no subscription when the account is newly created
        and is on the free period.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
            seasonality_credit=3,
            subscribed=False
        )
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-01&to=2021-07-05&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, False)

    def test_seasonality_analysis_view_successful_with_yes_scats_credit_yes_seasonality_credit_yes_subscription_newly_created_account(self):
        """
        Test that seasonality analysis view is successful with scats credit,
        seasonality credit, subscription when the account is newly created and is on the free period.
        """
        client = APIClient()
        user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP',
            scats_credit=3,
            seasonality_credit=3,
            subscribed=True
        )
        client.force_authenticate(user=user)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, True)

        res = client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-07-01&to=2021-07-05&detectors=all'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(user.scats_credit, 3)
        self.assertEqual(user.seasonality_credit, 3)
        self.assertEqual(user.subscribed, True)
