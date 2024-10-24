from django.urls.conf import include
from rest_framework import routers
from django.urls import path
from rest_framework.routers import DefaultRouter

from Train_Station_API_Service import settings
from station.views import (
    StationViewSet,
    RouteViewSet,
    CrewViewSet,
    TrainTypeViewSet,
    TrainViewSet,
    JourneyViewSet,
    TicketViewSet,
    OrderViewSet,
)

app_name = "train-station-ap1"

router = routers.DefaultRouter()
router.register("stations", StationViewSet, basename="stations")
router.register("routes", RouteViewSet, basename="routes")
router.register("crews", CrewViewSet, basename="crews")
router.register("train-types", TrainTypeViewSet, basename="train_types")
router.register("train", TrainViewSet, basename="train")
router.register("journeys", JourneyViewSet, basename="journeys")
router.register("orders", OrderViewSet, basename="orders")
router.register("tickets", TicketViewSet, basename="tickets")

urlpatterns = [
    path("", include(router.urls), name="station"),
]