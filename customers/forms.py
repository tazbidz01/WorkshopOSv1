from django import forms
from .models import Customer, Vehicle, CustomerNote

class CustomerForm(forms.ModelForm):
    """Form to create and edit customer details."""
    class Meta:
        model = Customer
        fields = [
            'name',
            'customer_type',
            'phone',
            'email',
            'address',
            'city',
            'country',
            'preferred_contact',
            'customer_since',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Mr. Rahman'}),
            'customer_type': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+880 1712 345678'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'rahman@example.com'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Dhanmondi, Dhaka 1209'}),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            'country': forms.TextInput(attrs={'class': 'form-input'}),
            'preferred_contact': forms.Select(attrs={'class': 'form-select'}),
            'customer_since': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }


class VehicleForm(forms.ModelForm):
    """Form to register a new vehicle under a customer."""
    class Meta:
        model = Vehicle
        fields = [
            'make',
            'model',
            'year',
            'engine_spec',
            'license_plate',
            'vin',
            'mileage',
            'image_url',
        ]
        widgets = {
            'make': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Toyota'}),
            'model': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Land Cruiser'}),
            'year': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '2021'}),
            'engine_spec': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'V8 4.5L Diesel'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'WB-1023'}),
            'vin': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'JTMHY05J404012345'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '186450'}),
            'image_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
        }


class CustomerNoteForm(forms.ModelForm):
    """Form to append staff notes for a customer."""
    class Meta:
        model = CustomerNote
        fields = ['content', 'author_name']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Add internal notes or customer preferences...'}),
            'author_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Staff Name'}),
        }
