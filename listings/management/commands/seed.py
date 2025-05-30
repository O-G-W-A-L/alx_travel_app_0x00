from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing, Booking, Review
from django.utils import timezone
import random
from faker import Faker
from datetime import timedelta

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = "Seed database with sample listings, bookings, and reviews"

    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")

        # Optional: Clear data
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()

        # Create or reuse test users
        host, _ = User.objects.get_or_create(username='host_user', email='host@example.com')
        host.set_password('testpass123')
        host.save()

        guest, _ = User.objects.get_or_create(username='guest_user', email='guest@example.com')
        guest.set_password('testpass123')
        guest.save()

        # Create Listings
        listings = []
        for _ in range(10):
            listings.append(Listing(
                host=host,
                title=fake.sentence(),
                description=fake.paragraph(),
                price_per_night=random.randint(50, 500),
                location=fake.city(),
                amenities=random.sample(["Wifi", "Pool", "Kitchen", "Parking", "TV"], k=random.randint(1, 3))
            ))
        Listing.objects.bulk_create(listings)
        listings = Listing.objects.all()  # Re-fetch to get IDs

        # Create Bookings
        bookings = []
        for listing in listings:
            check_in = timezone.now() + timedelta(days=random.randint(1, 30))
            bookings.append(Booking(
                listing=listing,
                guest=guest,
                check_in=check_in.date(),
                check_out=(check_in + timedelta(days=random.randint(1, 14))).date()
            ))
        Booking.objects.bulk_create(bookings)

        # Create Reviews
        reviews = []
        for listing in listings:
            reviews.append(Review(
                listing=listing,
                reviewer=guest,
                rating=random.randint(1, 5),
                comment=fake.paragraph() if random.random() > 0.3 else ""
            ))
        Review.objects.bulk_create(reviews)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
