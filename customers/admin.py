from django.contrib import admin
from .models import Customer, Vehicle, CustomerNote

class VehicleInline(admin.TabularInline):
    model = Vehicle
    extra = 1

class CustomerNoteInline(admin.StackedInline):
    model = CustomerNote
    extra = 1

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer_type', 'phone', 'email', 'city', 'preferred_contact', 'customer_since')
    list_filter = ('customer_type', 'preferred_contact', 'city')
    search_fields = ('name', 'phone', 'email', 'vehicles__license_plate')
    inlines = [VehicleInline, CustomerNoteInline]

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'license_plate', 'customer', 'mileage')
    search_fields = ('make', 'model', 'license_plate', 'vin', 'customer__name')
    list_filter = ('make', 'year')

@admin.register(CustomerNote)
class CustomerNoteAdmin(admin.ModelAdmin):
    list_display = ('customer', 'author_name', 'created_at')
    search_fields = ('customer__name', 'content', 'author_name')
