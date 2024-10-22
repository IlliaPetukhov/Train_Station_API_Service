from rest_framework import serializers


from station.models import (
    Station,
    Route,
    Ticket,
    Train,
    TrainType,
    Journey,
    Crew, Order
)


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ["id", "name", "latitude", "longitude"]


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        source = serializers.CharField(
            source="source.name",
            read_only=True,
        )
        destination = serializers.CharField(
            source="destination.name",
            read_only=True,
        )
        fields = ("id", "source", "destination", "distance")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ["id", "first_name", "last_name"]


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ["id", "name", "image"]


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        train_types = TrainTypeSerializer(many=False)
        fields = ["id", "name", "cargo_num", "places_in_cargo", "train_type"]


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        route = serializers.CharField(source="route.route_name")
        train = serializers.CharField(source="train.train_ihfo")
        fields = ["id", "route", "departure_time", "arrival_time"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["created_at", "user"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        journey = JourneySerializer(many=False)
        order = OrderSerializer(many=False)
        fields = ["cargo", "seats", "journey", "order"]

