from django.db import models
from rest_framework import serializers


class Iata(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    iata_code = models.CharField(max_length=3, blank=False, unique=True)


class IataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iata
        fields = ("iata_code",)


class Airport(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    iata = models.ForeignKey(
        Iata, on_delete=models.CASCADE, related_name="airport", to_field="iata_code"
    )
    city = models.CharField(max_length=100, blank=False)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    state = models.CharField(max_length=2, blank=False)


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("iata", "city", "latitude", "longitude", "state")
