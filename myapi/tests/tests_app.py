from .tests_base import BaseTest
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from myapi.views import get_person_info_list_view, get_sleep_info_list_view


class TestViews(BaseTest):
    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "myapi/index.html")

    def test_get_visualize_list_view(self):
        response = self.client.get(reverse("visualize-list-view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "myapi/visualize_list.html")

    def test_get_person_info_list_view_with_person_id(self):
        response = self.client.get(reverse("person-info-list") + "?person_id=1")
        self.assertRedirects(response, reverse("person-info-id", kwargs={"person_id": 1}))

    def test_get_person_info_list_view_without_person_id(self):
        response = self.client.get(reverse("person-info-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

    def test_get_sleep_info_list_view_with_sleep_id(self):
        response = self.client.get(reverse("sleep-info-list") + "?sleep_id=1")
        self.assertRedirects(response, reverse("sleep-info-id", kwargs={"sleep_id": 1}))

    def test_get_sleep_info_list_view_without_sleep_id(self):
        response = self.client.get(reverse("sleep-info-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

    def test_get_sleep_visualize_view_with_person_id(self):
        response = self.client.get(reverse("sleep-view") + "?person_id=1")
        self.assertRedirects(response, reverse("sleep-detail", kwargs={"person_id": 1}))
