from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from station.permissions import IsAdminOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiParameter
from station.paginations import (
    PaginationForShortSerializerData,
    PaginationForLongSerializerData,
    PaginationForTooLongSerializerData,
)
from datetime import datetime


from station.models import (
    Station,
    Route,
    Crew,
    TrainType,
    Train,
    Journey,
    Order,
    Ticket
)

from station.serializers import (
    StationSerializer,
    CrewSerializer,
    TrainTypeSerializer,
    OrderSerializerPost,
    TrainSerializerPost,
    TrainSerializerGet,
    JourneySerializerGet,
    JourneySerializerPost,
    TicketSerializerGet,
    TicketSerializerPost,
    RouteSerializerGet,
    RouteSerializerPost, OrderSerializerGet
)

class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    pagination_class = PaginationForShortSerializerData
    permission_classes = (IsAdminOrReadOnly, )


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    pagination_class = PaginationForShortSerializerData
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return RouteSerializerGet
        return RouteSerializerPost


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    pagination_class = PaginationForShortSerializerData
    permission_classes = (IsAdminOrReadOnly,)


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer
    pagination_class = PaginationForShortSerializerData
    permission_classes = (IsAdminOrReadOnly,)


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    pagination_class = PaginationForLongSerializerData
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return TrainSerializerGet

        return TrainSerializerPost


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    pagination_class = PaginationForLongSerializerData
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return JourneySerializerGet

        return JourneySerializerPost
    
    def get_queryset(self):
        departure_time = self.request.query_params.get("departure_time")
        route = self.request.query_params.get("route")
        if departure_time:
            departure_time = (datetime.strptime
                              (departure_time,"%Y-%m-%d").date())
            return (Journey.objects.filter
                    (departure_time__gte=departure_time))
        if route:
            return Journey.objects.filter(route=route)
        return Journey.objects.all()
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="departure_time",
                description="filter by departure time",
            ),
            OpenApiParameter(
                name="route",
                description="filter by route",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializerPost
    pagination_class = PaginationForTooLongSerializerData
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list" or (self.action == "retrieve" and
                                     self.request.method == "GET"):
            return OrderSerializerGet
        return OrderSerializerPost


class TicketViewSet(viewsets.ModelViewSet):
    pagination_class = PaginationForTooLongSerializerData
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TicketSerializerGet
        return TicketSerializerPost
