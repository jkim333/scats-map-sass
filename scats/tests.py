from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse


class PublicScatsApiTests(TestCase):
    """Test the publicly available scats API"""
    def setUp(self):
        self.client = APIClient()
    
    def test_access_to_opsheet_download_view_fails(self):
        """
        Test that access to opsheet download view fails.
        """
        request = self.client.get(
            reverse('scats:opsheet-download', kwargs={'scats_id': 100})
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_to_extract_scats_data_view_fails(self):
        """
        Test that access to extract scats data view fails.
        """
        request = self.client.get(
            reverse('scats:extract-scats-data')+'?scats_id=100&from=2021-06-10&to=2021-06-17'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_to_seasonality_analysis_view_fails(self):
        """
        Test that access to seasonality analysis view fails.
        """
        request = self.client.get(
            reverse('scats:seasonality-analysis')+'?scats_id=100&from=2021-06-10&to=2022-06-09&detectors=all'
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUsersApiTests(TestCase):
    """Test the private users API"""
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            company_name='3DP'
        )
        cls.client.force_authenticate(user=cls.user)
        # TODO: create scats objects.

    def test_access_to_extract_scats_data_view_with_no_scats_credit_no_seasonality_credit_no_subscription_fails(self):
        """
        Test that access to extract scats data view fails with
        no scats credit, no seasonality credit and no subscription.
        """
        pass

    def test_access_to_extract_scats_data_view_with_no_scats_credit_yes_seasonality_credit_no_subscription_fails(self):
        """
        Test that access to extract scats data view fails with
        no scats credit, yes seasonality credit and no subscription.
        """
        pass

    def test_access_to_extract_scats_data_view_with_no_scats_credit_no_seasonality_credit_yes_subscription_succeeds(self):
        """
        Test that access to extract scats data view succeeds with
        no scats credit, no seasonality credit and yes subscription.
        """
        pass

    def test_access_to_extract_scats_data_view_with_yes_scats_credit_no_seasonality_credit_no_subscription_succeeds(self):
        """
        Test that access to extract scats data view succeeds with
        yes scats credit, no seasonality credit and no subscription.
        """
        pass

    def test_access_to_extract_scats_data_view_with_yes_scats_credit_yes_seasonality_credit_yes_subscription_does_not_deduct_any_credit(self):
        """
        Test that access to extract scats data view with
        yes scats credit, yes seasonality credit and yes subscription
        does not deduct any credit points.
        """
        pass

    def test_access_to_extract_scats_data_view_with_invalid_scats_id_fails(self):
        """
        Test that access to extract scats data view with invalid scats_id fails.
        """
        pass

    def test_access_to_extract_scats_data_view_with_invalid_from_fails(self):
        """
        Test that access to extract scats data view with invalid from fails.
        +
        Test that from date is greater than the minimum database date.
        """
        pass

    def test_access_to_extract_scats_data_view_with_invalid_to_fails(self):
        """
        Test that access to extract scats data view with invalid to fails.
        +
        Test that to date is less than the maximum database date.
        """
        pass

    def test_access_to_extract_scats_data_view_with_difference_between_from_and_to_more_than_seven_days_fails(self):
        """
        Test that access to extract scats data view with the difference between
        from and to dates more than 7 days fails.
        """
        pass

    def test_access_to_extract_scats_data_view_with_from_greater_than_or_equal_to_to_fails(self):
        """
        Test that access to extract scats view with from date greater
        than or equal to to date fails.
        """
        pass

    def test_access_to_extract_scats_data_view_fails_if_no_data_found(self):
        """
        Test that access to extract scats data view fails if there was no data
        found.
        """
        pass

    def test_access_to_extract_scats_data_view_with_valid_inputs_succeeds(self):
        """
        Test that access to extract scats data view with valid inputs is successful.
        """
        pass

    def test_access_to_seasonality_analysis_view_with_no_scats_credit_no_seasonality_credit_no_subscription_fails(self):
        """
        Test that access to seasonality analysis view fails with
        no scats credit, no seasonality credit and no subscription.
        """
        pass

    def test_access_to_seasonality_analysis_view_with_no_scats_credit_yes_seasonality_credit_no_subscription_succeeds(self):
        """
        Test that access to seasonality analysis view succeeds with
        no scats credit, yes seasonality credit and no subscription.
        """
        pass

    def test_access_to_seasonality_analysis_view_with_no_scats_credit_no_seasonality_credit_yes_subscription_succeeds(self):
        """
        Test that access to seasonality analysis view succeeds with
        no scats credit, no seasonality credit and yes subscription.
        """
        pass

    def test_access_to_seasonality_analysis_view_with_yes_scats_credit_no_seasonality_credit_no_subscription_fails(self):
        """
        Test that access to seasonality analysis view fails with
        yes scats credit, no seasonality credit and no subscription.
        """
        pass

    def test_access_to_seasonality_analysis_view_with_yes_scats_credit_yes_seasonality_credit_yes_subscription_does_not_deduct_any_credit(self):
        """
        Test that access to seasonality analysis view with
        yes scats credit, yes seasonality credit and yes subscription
        does not deduct any credit points.
        """
        pass

    def test_access_to_seasonality_analysis_view_with_invalid_scats_id_fails(self):
        """
        Test that access to seasonality analysis view with invalid scats_id fails.
        """
        pass

    def test_access_to_seasonality_analysis_view_with_invalid_from_fails(self):
        """
        Test that access to seasonality analysis view with invalid from fails.
        +
        Test that from date is greater than the minimum database date.
        """
        pass

    def test_access_to_seasonality_analysis_view_with_invalid_to_fails(self):
        """
        Test that access to seasonality analysis view with invalid to fails.
        +
        Test that to date is less than the maximum database date.
        """
        pass

    def test_access_to_seasonality_analysis_view_with_difference_between_from_and_to_more_than_three_hundred_sixty_five_days_fails(self):
        """
        Test that access to seasonality analysis view with the difference between from and to dates more than 365 days fails.
        """
        pass

    def test_access_to_seasonality_analysis_view_with_from_greater_than_or_equal_to_to_fails(self):
        """
        Test that access to seasonality analysis view with from date greater
        than or equal to to date fails.
        """
        pass

    def test_access_to_seasonality_analysis_view_with_invalid_detectors_fails(self):
        """
        Test that access to seasonality analysis view with invalid detectors fails.
        """
        pass

    def test_access_to_seasonality_analysis_view_with_detectors_all_or_none_produces_outputs_for_all_detectors(self):
        """
        Test that access to seasonality analysis view with detectors equal to
        'all' or None produces output for all detectors.
        """
        pass

    def test_access_to_seasonality_analysis_view_with_specific_detectors_produces_outputs_for_specific_detectors(self):
        """
        Test that access to seasonality analysis view with specific detectors
        produces outputs for specific detectors.
        """
        pass

    def test_access_to_seasonality_analysis_view_fails_if_no_data_found(self):
        """
        Test that access to seasonality analysis view fails if there was no data
        found.
        """
        pass

    def test_access_to_seasonality_analysis_view_with_valid_inputs_succeeds(self):
        """
        Test that access to seasonality analysis view with valid inputs is successful.
        """
        pass
