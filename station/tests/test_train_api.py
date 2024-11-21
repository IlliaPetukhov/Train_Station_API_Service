
import datetime


from django.db.models import Count, F
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse


STATION_LIST_URL = "/train-station-ap1/stations/"
# ROUTE_LIST_URL = reverse("station:route-list")
# CREW_LIST_URL = reverse("station:crew-list")
# TRAIN_TYPE_LIST_URL = reverse("station:train-type-list")
# TRAIN_LIST_URL = reverse("station:train-list")
# JOURNEY_LIST_URL = reverse("station:journey-list")
# ORDER_LIST_URL = reverse("station:order-list")
# TICKET_LIST_URL = reverse("station:ticket-list")


class TestsAllModelsForUnauthorizedUser(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_user_station(self):
        response = self.client.get(STATION_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_unauthorized_user_route(self):
#         response = self.client.get(ROUTE_LIST_URL)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_unauthorized_user_crew(self):
#         response = self.client.get(CREW_LIST_URL)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_unauthorized_user_train_type(self):
#         response = self.client.get(TRAIN_TYPE_LIST_URL)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_unauthorized_user_train(self):
#         response = self.client.get(TRAIN_LIST_URL)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_unauthorized_user_journey(self):
#         response = self.client.get(JOURNEY_LIST_URL)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_unauthorized_user_order(self):
#         response = self.client.get(ORDER_LIST_URL)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class TestsStationsForAuthorizedUser(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)