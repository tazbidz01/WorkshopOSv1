from django.db import models
from django.utils import timezone
from datetime import date

class Customer(models.Model):
    """
    Stores customer profile information, contact details, and preferences.
    Corresponds to Table 4 ('Customers') in the WorkshopOS Data Model.
    """
    CUSTOMER_TYPE_CHOICES = [
        ('REGULAR', 'Regular Customer'),
        ('VIP', 'VIP Customer'),
        ('CORPORATE', 'Corporate Client'),
        ('NEW', 'New Customer'),
    ]

    PREFERRED_CONTACT_CHOICES = [
        ('Phone', 'Phone'),
        ('Email', 'Email'),
        ('WhatsApp', 'WhatsApp'),
        ('SMS', 'SMS'),
    ]

    name = models.CharField(max_length=150, help_text="Full Name (e.g., Mr. Rahman)")
    customer_type = models.CharField(
        max_length=20,
        choices=CUSTOMER_TYPE_CHOICES,
        default='REGULAR',
        help_text="Customer status tier"
    )
    phone = models.CharField(max_length=30, help_text="Contact number (+880...)")
    email = models.EmailField(help_text="Primary email address")
    address = models.CharField(max_length=255, default="Dhanmondi, Dhaka 1209")
    city = models.CharField(max_length=100, default="Dhaka")
    country = models.CharField(max_length=100, default="Bangladesh")
    preferred_contact = models.CharField(
        max_length=20,
        choices=PREFERRED_CONTACT_CHOICES,
        default='Phone'
    )
    customer_since = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.name

    @property
    def initials(self):
        """Returns initials for avatar (e.g. 'MR' for 'Mr. Rahman')."""
        parts = self.name.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[1][0]}".upper()
        elif parts:
            return parts[0][:2].upper()
        return "CU"

    @property
    def member_duration_display(self):
        """Displays duration as customer (e.g., '3 years, 7 months')."""
        today = date.today()
        years = today.year - self.customer_since.year
        months = today.month - self.customer_since.month
        if months < 0:
            years -= 1
            months += 12
        return f"{years} years, {months} months" if years > 0 else f"{months} months"


class Vehicle(models.Model):
    """
    Stores vehicle specifications, registration details, and customer ownership.
    Corresponds to Table 5 ('Vehicles') in the WorkshopOS Data Model.
    """
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='vehicles'
    )
    make = models.CharField(max_length=50, help_text="Manufacturer (e.g. Toyota, BMW)")
    model = models.CharField(max_length=50, help_text="Model name (e.g. Land Cruiser, 530i)")
    year = models.PositiveIntegerField(default=2020)
    engine_spec = models.CharField(max_length=100, blank=True, help_text="e.g. V8 4.5L Diesel or 2.0L Turbo Petrol")
    license_plate = models.CharField(max_length=30, unique=True, help_text="License plate (e.g. WB-1023)")
    vin = models.CharField(max_length=50, blank=True, null=True, help_text="Vehicle Identification Number")
    mileage = models.PositiveIntegerField(default=0, help_text="Current mileage in km")
    image_url = models.URLField(blank=True, null=True, help_text="URL to vehicle photo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"


class CustomerNote(models.Model):
    """
    Internal workshop notes regarding customer preferences, instructions, or history.
    """
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    content = models.TextField(help_text="Detailed note body")
    author_name = models.CharField(max_length=100, default="Ibrahim Khan (Admin)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note by {self.author_name} for {self.customer.name}"
