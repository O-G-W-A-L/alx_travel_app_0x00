from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class Listing(models.Model):
    """Property listing (e.g., Airbnb-style rental)"""
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    location = models.CharField(max_length=200)
    amenities = models.JSONField(default=list)  # e.g., ["Wifi", "Pool"]
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['price_per_night']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return f"{self.title} (${self.price_per_night}/night)"

class Booking(models.Model):
    """Reservation for a Listing"""
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    guest = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(check_out__gt=models.F('check_in')),
                name='check_out_after_check_in'
            ),
            models.UniqueConstraint(
                fields=['listing', 'check_in', 'check_out'],
                name='unique_booking_dates'
            )
        ]

    def __str__(self):
        return f"Booking #{self.id} for {self.listing.title}"

class Review(models.Model):
    """Guest review for a Listing"""
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['listing', 'reviewer']  # Prevent duplicate reviews
        indexes = [
            models.Index(fields=['listing']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f"{self.rating}★ by {self.reviewer.username}"