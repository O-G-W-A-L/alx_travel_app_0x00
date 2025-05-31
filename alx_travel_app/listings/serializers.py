from rest_framework import serializers
from .models import Listing, Booking, Review
from django.utils import timezone

class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model."""
    
    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['host', 'created_at', 'updated_at']

class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model with custom validations."""
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['guest', 'created_at']

    def validate_check_in(self, value):
        """Validate that the check-in date is in the future."""
        if value < timezone.now().date():
            raise serializers.ValidationError("Check-in date must be in the future.")
        return value

    def validate(self, data):
        """Check for conflicting bookings."""
        if 'check_out' in data and 'listing' in data:
            conflicting_bookings = Booking.objects.filter(
                listing=data['listing'],
                check_out__gt=data['check_in'],
                check_in__lt=data['check_out']
            ).exists()
            if conflicting_bookings:
                raise serializers.ValidationError("These dates are already booked.")
        return data

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['reviewer', 'created_at']

    def validate_rating(self, value):
        """Ensure rating is between 1 and 5."""
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value