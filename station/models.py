from django.contrib.auth.models import User
from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="routes_from")
    destination = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="routes_to"
    )
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source.name} - {self.destination.name}"

    @property
    def route_name(self):
        return f"{self.source.name} - {self.destination.name}"


class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TrainType(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="train_types")

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=100)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(TrainType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def train_info(self):
        return f"Train_type: {self.train_type.name}, Train name: {self.name}"


class Journey(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.route} - {self.train.name} - {self.train.train_type.name}"

    @property
    def route_name(self):
        return f"{self.route} - {self.train}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.created_at} - {self.user}"


class Ticket(models.Model):
    cargo = models.IntegerField()
    seats = models.IntegerField()
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets", null=True)

    def __str__(self):
        return f"{self.journey}"


    @property
    def seat(self):
        return f"{self.seats}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["cargo", "seats"], name="unique_cargo_seat")
        ]
