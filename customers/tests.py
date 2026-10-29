from django.test import TestCase, Client
from django.urls import reverse
from .models import Customer, Vehicle, CustomerNote
from datetime import date

class CustomerModelTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Mr. Rahman",
            customer_type="REGULAR",
            phone="+880 1712 345678",
            email="rahman@example.com",
            address="Dhanmondi, Dhaka 1209",
            city="Dhaka",
            country="Bangladesh",
            preferred_contact="Phone",
            customer_since=date(2021, 3, 1)
        )

    def test_customer_creation_and_properties(self):
        self.assertEqual(str(self.customer), "Mr. Rahman")
        self.assertEqual(self.customer.initials, "MR")
        self.assertIn("years", self.customer.member_duration_display)

    def test_vehicle_association(self):
        vehicle = Vehicle.objects.create(
            customer=self.customer,
            make="Toyota",
            model="Land Cruiser",
            year=2011,
            engine_spec="V8 4.5L Diesel",
            license_plate="WB-1023",
            mileage=186450
        )
        self.assertEqual(self.customer.vehicles.count(), 1)
        self.assertEqual(str(vehicle), "Toyota Land Cruiser (WB-1023)")

    def test_note_creation(self):
        note = CustomerNote.objects.create(
            customer=self.customer,
            content="Prefers genuine OEM parts.",
            author_name="Ibrahim Khan"
        )
        self.assertEqual(self.customer.notes.count(), 1)
        self.assertEqual(note.author_name, "Ibrahim Khan")


class CustomerViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = Customer.objects.create(
            name="Mr. Rahman",
            customer_type="REGULAR",
            phone="+880 1712 345678",
            email="rahman@example.com",
            address="Dhanmondi, Dhaka 1209",
            city="Dhaka",
            country="Bangladesh",
            preferred_contact="Phone",
        )
        self.vehicle = Vehicle.objects.create(
            customer=self.customer,
            make="Toyota",
            model="Land Cruiser",
            year=2011,
            license_plate="WB-1023"
        )

    def test_profile_view_default(self):
        response = self.client.get(reverse('customers:profile_default'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/profile.html')
        self.assertContains(response, "Mr. Rahman")
        self.assertContains(response, "Toyota Land Cruiser")
        self.assertContains(response, "WB-1023")

    def test_profile_view_by_id(self):
        response = self.client.get(reverse('customers:profile', args=[self.customer.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mr. Rahman")

    def test_customer_list_view(self):
        response = self.client.get(reverse('customers:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/list.html')
        self.assertContains(response, "Mr. Rahman")

    def test_customer_search(self):
        response = self.client.get(reverse('customers:list') + '?q=Rahman')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mr. Rahman")

        response = self.client.get(reverse('customers:list') + '?q=NonExistent')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No customers found")

    def test_customer_edit(self):
        response = self.client.post(
            reverse('customers:edit', args=[self.customer.id]),
            {
                'name': 'Mr. Rahman Updated',
                'customer_type': 'VIP',
                'phone': '+880 1999 888777',
                'email': 'updated@example.com',
                'address': 'Gulshan 2, Dhaka',
                'city': 'Dhaka',
                'country': 'Bangladesh',
                'preferred_contact': 'WhatsApp',
                'customer_since': '2021-03-01'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, 'Mr. Rahman Updated')
        self.assertEqual(self.customer.customer_type, 'VIP')
        self.assertEqual(self.customer.phone, '+880 1999 888777')

    def test_add_vehicle_action(self):
        response = self.client.post(
            reverse('customers:add_vehicle', args=[self.customer.id]),
            {
                'make': 'BMW',
                'model': '530i',
                'year': 2018,
                'engine_spec': '2.0L Turbo Petrol',
                'license_plate': 'WB-7781',
                'vin': 'WBAJA7C01FF8012648',
                'mileage': 72300,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.customer.vehicles.count(), 2)
        self.assertTrue(Vehicle.objects.filter(license_plate='WB-7781').exists())

    def test_add_note_action(self):
        response = self.client.post(
            reverse('customers:add_note', args=[self.customer.id]),
            {
                'author_name': 'Ibrahim Khan',
                'content': 'Test preference note for workshop.'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.customer.notes.count(), 1)
        self.assertEqual(self.customer.notes.first().content, 'Test preference note for workshop.')
