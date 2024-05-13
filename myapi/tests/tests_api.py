from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from myapi.serializers import *
from .tests_base import BaseTest


class TestAPI(BaseTest):
    def test_sleep_info_list_by_date(self):
        """Test retrieving a list of Sleep information by date"""
        dt = timezone.now()
        url = reverse('sleep-info-list') + f"?day={dt.day}&month={dt.month}&year={dt.year}"
        response = self.client.get(url)

        # Check if the request was successful (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.set_linked()
        # Check if the response data matches the expected serialized data
        expected_data = SleepInfoSerializer([self.sleepA1, self.sleepB1, self.sleepC1, self.sleepD1], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_sleep_info_list_by_specific_date(self) -> None:
        """Test retrieving a list of Sleep information by specific date"""
        dt = timezone.now() - timedelta(days=1)
        url = reverse('sleep-info-list') + f"?day={dt.day}"
        response = self.client.get(url)

        # Check if the request was successful (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.set_linked()
        # Check if the response data matches the expected serialized data
        expected_data = SleepInfoSerializer([self.sleepA2, self.sleepB2, self.sleepC2, self.sleepD2], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_get_sleep_info_list(self):
        """Test retrieving a list of sleep information with the closest environment data."""
        url = reverse('sleep-info-list')
        response = self.client.get(url)

        # Check if the request was successful (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the response data matches the expected serialized data
        self.set_linked()
        expected_data = SleepInfoSerializer(self.get_sleep_list(), many=True).data
        self.assertEqual(response.data, expected_data)

    def test_get_sleep_info_by_id(self):
        """Test retrieving detailed sleep information by sleep_id."""
        url = reverse('sleep-info-id', args=[self.sleepA1.sleep_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.set_linked()
        expected_data = SleepInfoSerializer(self.sleepA1).data
        self.assertEqual(response.data, expected_data)

    def test_get_sleep_info_by_person(self):
        """Test retrieving sleep information for a specific person."""
        # Construct the URL for retrieving sleep info by person ID
        url = reverse('sleep-info-person', args=[self.personA.person_id])
        response = self.client.get(url)

        # Check if the request was successful (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data matches the expected serialized data
        self.set_linked()
        expected_data = SleepInfoSerializer([self.sleepA1, self.sleepA2], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_get_sleep_info_by_location_default(self):
        """Test retrieving sleep information by location."""
        # Construct the URL for retrieving sleep info by location within default range
        url_default_range = reverse('sleep-info-location-within-5-km',
                                    kwargs={'lat': 0.03, 'lon': 0.03})
        response_default_range = self.client.get(url_default_range)
        # Check if the request with default range was successful (HTTP 200 OK)
        self.assertEqual(response_default_range.status_code, status.HTTP_200_OK)

        # Check if the response data with default range matches the expected serialized data
        self.set_linked()
        expected_data_default_range = SleepInfoSerializer(
            self.get_sleep_list([self.sleepB1, self.sleepB2]),
            many=True).data
        # print([i['sleep_id'] for i in expected])
        self.assertEqual(response_default_range.data, expected_data_default_range)

    def test_get_sleep_info_by_location(self):
        """Test retrieving sleep information by location."""
        # Construct the URL for retrieving sleep info by location within specified range (10000 km)
        url_specified_range = reverse('sleep-info-location-within-range',
                                      kwargs={'lat': 0.03, 'lon': 0.03, 'km': 10000})
        response_specified_range = self.client.get(url_specified_range)

        # Check if the request with specified range was successful (HTTP 200 OK)
        self.assertEqual(response_specified_range.status_code, status.HTTP_200_OK)

        # Check if the response data with specified range matches the expected serialized data
        self.set_linked()
        expected_data_specified_range = SleepInfoSerializer(self.get_sleep_list(), many=True).data
        self.assertEqual(response_specified_range.data, expected_data_specified_range)

    def test_get_person_info_list(self):
        """Test retrieving a list of Person information."""
        url = reverse('person-info-list')
        response = self.client.get(url)

        # Check if the request was successful (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data matches the expected serialized data
        expected_data = PersonInfoSerializer(
            [self.personA, self.personB, self.personC, self.personD], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_get_person_info_by_id(self):
        """Test retrieving detailed information about a specific person."""
        url = reverse('person-info-id', args=[self.personA.person_id])
        response = self.client.get(url)

        # Check if the request was successful (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data matches the expected serialized data
        expected_data = PersonInfoSerializer(self.personA).data
        self.assertEqual(response.data, expected_data)

    def test_get_sleep_analytics(self):
        """Test retrieving a list of sleep analytics for all persons."""
        url = reverse('sleep-analytics')
        response = self.client.get(url)

        # Check if the request was successful (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_sleep_analytics_by_person_id(self):
        """Test retrieving a list of sleep analytics for specific person."""
        url = reverse('sleep-analytics')
        response = self.client.get(url)

        # Check if the request was successful (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sleep_info_list_invalid_date(self):
        """Test retrieving a list of Person information."""
        dt = timezone.now()
        url = reverse('sleep-info-list') + "?day=32&month=13&year=2024"
        response = self.client.get(url)

        # Check if the request was successful (HTTP 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.set_linked()
        # Check if the response data matches the expected serialized data
        self.assertEqual(response.data, [])

    def test_sleep_info_non_exist_sleep_id(self):
        """Test retrieving a list of non-exsiting sleep information."""
        url = reverse('sleep-info-id', args=(9999,))
        response = self.client.get(url)

        # Check if the request was not found (HTTP 404 NOT FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_person_info_non_exist_person_id(self):
        """Test retrieving detailed information about a specific person."""
        url = reverse('person-info-id', args=(9999,))
        response = self.client.get(url)

        # Check if the request was not found (HTTP 404 NOT FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
