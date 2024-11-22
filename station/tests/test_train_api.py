import sys
from django.contrib.auth import get_user_model
import datetime
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from station.serializers import *

STATION_LIST_URL = "/train-station-ap1/stations/"
ROUTE_LIST_URL = "/train-station-ap1/routes/"
CREW_LIST_URL = "/train-station-ap1/crews/"
TRAIN_TYPE_LIST_URL = "/train-station-ap1/train-types/"
TRAIN_LIST_URL = "/train-station-ap1/train/"
JOURNEY_LIST_URL = "/train-station-ap1/journeys/"
ORDER_LIST_URL = "/train-station-ap1/orders/"
TICKET_LIST_URL = "/train-station-ap1/tickets/"

class TestsAllModelsForUnauthorizedUser(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthorized_user_station(self):
        response = self.client.get(STATION_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_route(self):
        response = self.client.get(ROUTE_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_crew(self):
        response = self.client.get(CREW_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_train_type(self):
        response = self.client.get(TRAIN_TYPE_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_train(self):
        response = self.client.get(TRAIN_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_journey(self):
        response = self.client.get(JOURNEY_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_order(self):
        response = self.client.get(ORDER_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestsAllModelsForAuthorizedUser(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username="Test", password="<PASSWORD>")
        self.client.force_authenticate(user=self.user)

        self.station_1 = Station.objects.create(
            name="Test Station",
            latitude=3.14,
            longitude=3.14
        )
        self.station_2 = Station.objects.create(
            name="Test Station 2",
            latitude=3.14,
            longitude=3.14
        )

        self.route_1 = Route.objects.create(
            source=self.station_1,
            destination=self.station_2,
            distance=345
        )
        self.route_2 = Route.objects.create(
            source=self.station_2,
            destination=self.station_1,
            distance=782
        )

        self.crew_1 = Crew.objects.create(
            first_name="Test 1",
            last_name="Test 1"
        )
        self.crew_2 = Crew.objects.create(
            first_name="Test 2",
            last_name="Test 2"
        )

        self.train_type_1 = TrainType.objects.create(
            name="Test Type",
            image=SimpleUploadedFile(
                name="test.jpg",
                content=b"",
                content_type="image/jpeg"
            )
        )

        self.train_1 = Train.objects.create(
            name="Test Train 1",
            cargo_num=9,
            places_in_cargo=40,
            train_type=self.train_type_1,
        )
        self.train_2 = Train.objects.create(
            name="Test Train 2",
            cargo_num=3,
            places_in_cargo=490,
            train_type=self.train_type_1,
        )

        self.journey_1 = Journey.objects.create(
            route=self.route_1,
            train=self.train_1,
            departure_time="2024-11-10T00:00:00Z",
            arrival_time="2024-11-12T00:00:00Z"
        )
        self.journey_2 = Journey.objects.create(
            route=self.route_2,
            train=self.train_2,
            departure_time="2024-12-10T00:00:00Z",
            arrival_time="2024-12-12T00:00:00Z"
        )

        self.order = Order.objects.create(
            created_at=datetime.datetime.now(),
            user=self.user,
        )

        self.ticket_1 = Ticket.objects.create(
            cargo=1,
            seats=1,
            journey=self.journey_1,
            order=self.order,
        )
        self.ticket_2 = Ticket.objects.create(
            cargo=2,
            seats=1,
            journey=self.journey_2,
            order=self.order,
        )


    def test_authorized_user_station(self):
        response = self.client.get(STATION_LIST_URL)
        station_serializer_1 = StationSerializer(self.station_1)
        station_serializer_2 = StationSerializer(self.station_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(station_serializer_1.data, response.data["results"][0])
        self.assertEqual(station_serializer_2.data, response.data["results"][1])
        self.assertNotEqual(station_serializer_2.data, response.data["results"][0])

    def test_station_post_for_authorized_user(self):
        response = self.client.post(STATION_LIST_URL, {"name": "test",
                                                       "latitude": 4, "longitude": 3},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_user_route(self):
        response = self.client.get(ROUTE_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        route_serializer_1 = RouteSerializerGet(self.route_1)
        route_serializer_2 = RouteSerializerGet(self.route_2)
        self.assertEqual(route_serializer_1.data, response.data["results"][0])
        self.assertEqual(route_serializer_2.data, response.data["results"][1])
        self.assertNotEqual(route_serializer_2.data, response.data["results"][0])

    def test_route_post_for_authorized_user(self):
        response = self.client.post(ROUTE_LIST_URL, {"source": self.station_1.id,
                                                       "destination": self.station_1.id,
                                                     "distance": 312},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_authorized_user_crew(self):
        response = self.client.get(CREW_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        crew_serializer_1 = CrewSerializer(self.crew_1)
        crew_serializer_2 = CrewSerializer(self.crew_2)
        self.assertEqual(crew_serializer_1.data, response.data["results"][0])
        self.assertEqual(crew_serializer_2.data, response.data["results"][1])
        self.assertNotEqual(crew_serializer_1.data, response.data["results"][1])

    def test_crew_post_for_authorized_user(self):
        response = self.client.post(ROUTE_LIST_URL, {"first_name": "distance",
                                                       "last_name": "distance"},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_user_train_type(self):
        response = self.client.get(TRAIN_TYPE_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        train_type_serializer_1 = TrainTypeSerializer(self.train_type_1)
        self.assertEqual(train_type_serializer_1.data["image"].split("/")[-1],
                         response.data["results"][0]["image"].split("/")[-1])


    def test_train_type_post_for_authorized_user(self):
        response = self.client.post(ROUTE_LIST_URL, {"name": "distance"},
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_authorized_user_train(self):
        response = self.client.get(TRAIN_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        train_serializer_1 = TrainSerializerGet(self.train_1)
        train_serializer_2 = TrainSerializerGet(self.train_2)
        self.assertEqual(train_serializer_1.data["name"], response.data["results"][0]["name"])
        self.assertEqual(train_serializer_1.data["cargo_num"], response.data["results"][0]["cargo_num"])
        self.assertEqual(train_serializer_1.data["places_in_cargo"], response.data["results"][0]["places_in_cargo"])
        self.assertEqual(train_serializer_1.data["train_type"]["image"].split("/")[-1],
                         response.data["results"][0]["train_type"]["image"].split("/")[-1])

        self.assertEqual(train_serializer_2.data["name"], response.data["results"][1]["name"])
        self.assertEqual(train_serializer_2.data["cargo_num"], response.data["results"][1]["cargo_num"])
        self.assertEqual(train_serializer_2.data["places_in_cargo"], response.data["results"][1]["places_in_cargo"])
        self.assertEqual(train_serializer_2.data["train_type"]["image"].split("/")[-1],
                         response.data["results"][1]["train_type"]["image"].split("/")[-1])


    def test_train_post_for_authorized_user(self):
        self.train_type_1 = TrainType.objects.create(
            name="Test Type",
            image=SimpleUploadedFile(
                name="test.jpg",
                content=b"",
                content_type="image/jpeg"
            )
        )
        response_post = self.client.post(TRAIN_LIST_URL,
                                         {"name": "Test",
                                          "cargo_num": 3,
                                          "places_in_cargo": 2,
                                          "train_type": self.train_type_1.id},
                                         format="json")
        self.assertEqual(response_post.status_code, status.HTTP_403_FORBIDDEN)


    def test_authorized_user_journey(self):
        response = self.client.get(JOURNEY_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        journey_serializer_1 = JourneySerializerGet(self.journey_1)
        journey_serializer_2 = JourneySerializerGet(self.journey_2)
        self.assertEqual(journey_serializer_1.data["route"],
                         response.data["results"][0]["route"])

        self.assertEqual(journey_serializer_1.data["departure_time"],
                         response.data["results"][0]["departure_time"])

        self.assertEqual(journey_serializer_1.data["arrival_time"],
                         response.data["results"][0]["arrival_time"])

        self.assertEqual(journey_serializer_2.data["route"],
                         response.data["results"][1]["route"])

        self.assertEqual(journey_serializer_2.data["departure_time"],
                         response.data["results"][1]["departure_time"])

        self.assertEqual(journey_serializer_2.data["arrival_time"],
                         response.data["results"][1]["arrival_time"])


    def test_journey_post_for_authorized_user(self):
        self.station_1 = Station.objects.create(
            name="Test Station",
            latitude=3.14,
            longitude=3.14
        )
        self.route_1 = Route.objects.create(
            source=self.station_1,
            destination=self.station_1,
            distance=345
        )
        self.train_type_1 = TrainType.objects.create(
            name="Test Type",
            image=SimpleUploadedFile(
                name="test.jpg",
                content=b"",
                content_type="image/jpeg"
            )
        )
        self.train_1 = Train.objects.create(
            name="Test Train 1",
            cargo_num=9,
            places_in_cargo=40,
            train_type=self.train_type_1,
        )

        response_post = self.client.post(JOURNEY_LIST_URL, {"route": self.route_1.id,
                                                            "train": self.train_1.id,
                                                            "departure_time": datetime.datetime.now(),
                                                            "arrival_time": datetime.datetime.now()},
                                         format="json")
        self.assertEqual(response_post.status_code, status.HTTP_403_FORBIDDEN)



    def test_authorized_user_ticket(self):
        response = self.client.get(TICKET_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ticket_serializer_1 = TicketSerializerGet(self.ticket_1)
        ticket_serializer_2 = TicketSerializerGet(self.ticket_2)
        self.assertEqual(ticket_serializer_1.data["cargo"],
                         response.data["results"][0]["cargo"])

        self.assertEqual(ticket_serializer_1.data["seats"],
                         response.data["results"][0]["seats"])

        self.assertEqual(ticket_serializer_1.data["seats"],
                         response.data["results"][0]["seats"])

        self.assertEqual(ticket_serializer_1.data["journey"]["route"],
                         response.data["results"][0]["journey"]["route"])

        self.assertEqual(ticket_serializer_2.data["cargo"],
                         response.data["results"][1]["cargo"])

        self.assertEqual(ticket_serializer_2.data["seats"],
                         response.data["results"][1]["seats"])

        self.assertEqual(ticket_serializer_2.data["seats"],
                         response.data["results"][1]["seats"])

        self.assertEqual(ticket_serializer_2.data["journey"]["route"],
                         response.data["results"][1]["journey"]["route"])


    def test_authorized_user_order(self):
        response = self.client.get(ORDER_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order_serializer_1 = OrderSerializerGet(self.order)
        self.assertEqual(order_serializer_1.data["user"],
                         response.data["results"][0]["user"])

        self.assertEqual(order_serializer_1.data["tickets"][0]["cargo"],
                         response.data["results"][0]["tickets"][0]["cargo"])

        self.assertEqual(order_serializer_1.data["tickets"][0]["seats"],
                         response.data["results"][0]["tickets"][0]["seats"])

        self.assertEqual(order_serializer_1.data["tickets"][0]["journey"]["route"],
                         response.data["results"][0]["tickets"][0]["journey"]["route"])

    def test_post_order_for_authorized_user(self):
        response = self.client.post(ORDER_LIST_URL, {
            "tickets": [
                {
                    "cargo": 1,
                    "seats": 2,
                    "journey": self.journey_1.id,
                }
            ]
        },
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_order_if_seat_alredy_in_use(self):
        response = self.client.post(ORDER_LIST_URL, {
            "tickets": [
                {
                    "cargo": 1,
                    "seats": 1,
                    "journey": self.journey_1.id,
                }
            ]
        },
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_if_cargo_more_then_max_possible_cargo(self):
        response = self.client.post(ORDER_LIST_URL, {
            "tickets": [
                {
                    "cargo": 999,
                    "seats": 1,
                    "journey": self.journey_1.id,
                }
            ]
        },
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_if_seat_more_then_max_possible_seat(self):
        response = self.client.post(ORDER_LIST_URL, {
            "tickets": [
                {
                    "cargo": 1,
                    "seats": 129101,
                    "journey": self.journey_1.id,
                }
            ]
        },
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_filter_journey_by_departure_time(self):
        response = self.client.get(JOURNEY_LIST_URL + "?departure_time=2024-11-10")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        journey_serializer_1 = JourneySerializerGet(self.journey_1)
        journey_serializer_2 = JourneySerializerGet(self.journey_2)
        self.assertEqual(journey_serializer_1.data["departure_time"], response.data["results"][0]["departure_time"])
        self.assertEqual(journey_serializer_2.data["departure_time"], response.data["results"][1]["departure_time"])
        self.assertNotEqual(journey_serializer_2.data["departure_time"], response.data["results"][0]["departure_time"])


    def test_filter_journey_by_route(self):
        response_1 = self.client.get(JOURNEY_LIST_URL + f"?route={self.route_1.id}")
        response_2 = self.client.get(JOURNEY_LIST_URL + f"?route={self.route_2.id}")
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        route_serializer_1 = RouteSerializerGet(self.route_1)
        route_serializer_2 = RouteSerializerGet(self.route_2)
        self.assertEqual(route_serializer_1.data, response_1.data["results"][0]["route"])
        self.assertEqual(route_serializer_2.data, response_2.data["results"][0]["route"])
        self.assertNotEqual(route_serializer_2.data, response_1.data["results"][0]["route"])

class TestAllModelsForAdmins(APITestCase):
    def setUp(self):
        self.user_admin = get_user_model().objects.create_superuser(username="Admin", password="<PASSWORD>")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_admin)


    def test_station_for_admin(self):
        response_post = self.client.post(STATION_LIST_URL, {"name": "Test Station",
                                    "latitude": 3, "longitude": 2}, format="json")
        response_get = self.client.get(STATION_LIST_URL)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response_get.data["results"], [])


    def test_route_for_admin(self):
        self.station_1 = Station.objects.create(
            name="Test Station",
            latitude=3.14,
            longitude=3.14
        )
        self.station_2 = Station.objects.create(
            name="Test Station 2",
            latitude=3.14,
            longitude=3.14
        )

        response_post = self.client.post(ROUTE_LIST_URL, {"source": self.station_1.id,
                                    "destination": self.station_2.id, "distance": 223}, format="json")
        response_get = self.client.get(ROUTE_LIST_URL)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response_get.data["results"], [])


    def test_crew_for_admin(self):
        response_post = self.client.post(CREW_LIST_URL, {"first_name": "last_name",
                                                          "last_name": "last_name", "distance": 223},
                                         format="json")
        response_get = self.client.get(CREW_LIST_URL)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response_get.data["results"], [])


    def test_train_type_for_admin(self):
        response_post = self.client.post(TRAIN_TYPE_LIST_URL,
                                          {"name": "Test Train Type"},
                                         format="json")
        response_get = self.client.get(TRAIN_TYPE_LIST_URL)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response_get.data["results"], [])


    def test_train_for_admin(self):
        self.train_type_1 = TrainType.objects.create(
            name="Test Type",
            image=SimpleUploadedFile(
                name="test.jpg",
                content=b"",
                content_type="image/jpeg"
            )
        )
        response_post = self.client.post(TRAIN_LIST_URL,
                                         {"name": "Test",
                                          "cargo_num": 3,
                                          "places_in_cargo": 2,
                                          "train_type": self.train_type_1.id},
                                         format="json")
        response_get = self.client.get(TRAIN_LIST_URL)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response_get.data["results"], [])


    def test_journey_for_admin(self):
        self.station_1 = Station.objects.create(
            name="Test Station",
            latitude=3.14,
            longitude=3.14
        )
        self.route_1 = Route.objects.create(
            source=self.station_1,
            destination=self.station_1,
            distance=345
        )
        self.train_type_1 = TrainType.objects.create(
            name="Test Type",
            image=SimpleUploadedFile(
                name="test.jpg",
                content=b"",
                content_type="image/jpeg"
            )
        )
        self.train_1 = Train.objects.create(
            name="Test Train 1",
            cargo_num=9,
            places_in_cargo=40,
            train_type=self.train_type_1,
        )

        response_post = self.client.post(JOURNEY_LIST_URL, {"route": self.route_1.id,
                                                            "train": self.train_1.id,
                                                            "departure_time": datetime.datetime.now(),
                                                            "arrival_time": datetime.datetime.now()},
                                         format="json")
        response_get = self.client.get(JOURNEY_LIST_URL)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response_get.data["results"], [])
