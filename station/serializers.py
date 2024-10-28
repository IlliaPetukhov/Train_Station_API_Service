from urllib import request

from django.contrib.auth.models import User
from rest_framework import serializers
from django.db import transaction
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField

from station.models import (
    Station,
    Route,
    Ticket,
    Train,
    TrainType,
    Journey,
    Crew, Order
)
from user.serializers import UserSerializer


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ["id", "name", "latitude", "longitude"]


class RouteSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteSerializerGet(serializers.ModelSerializer):
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
    route = RouteSerializerGet(read_only=True)
    train = TrainSerializerGet(read_only=True)

    class Meta:
        model = Journey
        fields = ["id", "route", "train", "departure_time", "arrival_time"]


class TicketSerializerGet(serializers.ModelSerializer):
    journey = JourneySerializerGet(many=False)

    class Meta:
        model = Ticket
        fields = ["cargo", "seats", "journey", "order"]


class TicketSerializerPost(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ["cargo", "seats", "journey"]

    def validate(self, attrs):
        cargo = attrs.get("cargo")
        seats = attrs.get("seats")
        journey = attrs.get("journey")
        max_cargo = journey.train.cargo_num
        max_seats = journey.train.places_in_cargo
        if Ticket.objects.filter(journey=journey, cargo=cargo, seats=seats).exists():
            raise serializers.ValidationError("This seat is already in use.")
        if int(cargo) > int(max_cargo):
            raise (serializers.ValidationError
                   ("The cargo in the ticket must be less than or equal to the maximum cargo."))
        if int(seats) > int(max_seats):
            raise (serializers.ValidationError
                   ("The seats in the ticket must be less than or equal to the maximum seats."))
        return attrs


class OrderSerializerPost(serializers.ModelSerializer):
    tickets = PrimaryKeyRelatedField(many=True, queryset=Ticket.objects.filter(order__isnull=True))
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["created_at", "user", "tickets"]


class OrderSerializerGet(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tickets = TicketSerializerGet(many=True)

    class Meta:
        model = Order
        fields = ["created_at", "user", "tickets"]
