# listings/serializers.py

from rest_framework import serializers
from .models import Listing, Booking


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for the Listing model."""

    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['host', 'created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for the Booking model."""

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['guest', 'created_at']

