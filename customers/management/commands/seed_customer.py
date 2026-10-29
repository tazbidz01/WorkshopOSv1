from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from customers.models import Customer, Vehicle, CustomerNote

class Command(BaseCommand):
    help = "Seed database with presentation data for Customer Profile (UI 03)"

    def handle(self, *args, **options):
        self.stdout.write("Seeding Customer Profile data...")

        customer, created = Customer.objects.get_or_create(
            name="Mr. Rahman",
            defaults={
                'customer_type': 'REGULAR',
                'phone': '+880 1712 345678',
                'email': 'rahman@example.com',
                'address': 'Dhanmondi, Dhaka 1209',
                'city': 'Dhaka',
                'country': 'Bangladesh',
                'preferred_contact': 'Phone',
                'customer_since': date(2021, 3, 1),
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created customer: {customer.name}"))
        else:
            self.stdout.write(f"Customer {customer.name} already exists.")

        # Seed Vehicles
        v1, v1_created = Vehicle.objects.get_or_create(
            license_plate='WB-1023',
            defaults={
                'customer': customer,
                'make': 'Toyota',
                'model': 'Land Cruiser',
                'year': 2011,
                'engine_spec': 'V8 4.5L Diesel',
                'vin': 'JTMHY05J404012345',
                'mileage': 186450,
            }
        )
        if v1_created:
            self.stdout.write(self.style.SUCCESS(f"Added vehicle: {v1.make} {v1.model} ({v1.license_plate})"))

        v2, v2_created = Vehicle.objects.get_or_create(
            license_plate='WB-7781',
            defaults={
                'customer': customer,
                'make': 'BMW',
                'model': '530i',
                'year': 2018,
                'engine_spec': '2.0L Turbo Petrol',
                'vin': 'WBAJA7C01FF8012648',
                'mileage': 72300,
            }
        )
        if v2_created:
            self.stdout.write(self.style.SUCCESS(f"Added vehicle: {v2.make} {v2.model} ({v2.license_plate})"))

        # Seed Notes
        if not customer.notes.exists():
            CustomerNote.objects.create(
                customer=customer,
                content="Prefers genuine OEM parts. Usually books service in advance. Keep the customer updated during service. Very particular about clean work and timely delivery.",
                author_name="Ibrahim Khan"
            )
            self.stdout.write(self.style.SUCCESS("Added customer preferences note."))

        self.stdout.write(self.style.SUCCESS("Customer Profile data seeded successfully!"))
