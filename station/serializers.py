from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

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
    source = serializers.CharField(
        source="source.name",
        read_only=True,
    )
    destination = serializers.CharField(
        source="destination.name",
        read_only=True,
    )

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ["id", "first_name", "last_name"]


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ["id", "name", "image"]


class TrainSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ["id", "name", "cargo_num", "places_in_cargo", "train_type"]


class TrainSerializerGet(serializers.ModelSerializer):
    train_type = TrainTypeSerializer(read_only=True)

    class Meta:
        model = Train
        fields = ["id", "name", "cargo_num", "places_in_cargo", "train_type"]


class JourneySerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = ["id", "route", "train", "departure_time", "arrival_time"]


class JourneySerializerGet(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    train = TrainSerializerGet(read_only=True)

    class Meta:
        model = Journey
        fields = ["id", "route", "train", "departure_time", "arrival_time"]


class TicketSerializerGet(serializers.ModelSerializer):
    journey = JourneySerializerGet(many=False)

    class Meta:
        model = Ticket
        fields = ["cargo", "seats", "journey"]


class TicketSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ["cargo", "seats", "journey"]


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ["created_at", "user", "tickets"]
