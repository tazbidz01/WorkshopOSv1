# WorkshopOS - Team Merge & Architecture Guide (CSE327)

This guide ensures all 4 team members can develop their assigned components independently in their own Git branches and merge them into `main` without merge conflicts or database dependency errors.

---

## 👥 Module Assignment Matrix

| Member | Assigned Component | Django App Name | Primary Responsibilities |
|---|---|---|---|
| **Member 1 (Current)** | **Customer Profile** | `customers/` | Profile details, editing, customer info, vehicle association, notes, stats |
| **Member 2** | **Job Card** | `jobs/` | Job numbers, customer, vehicle, assigned workshop, complaint, status |
| **Member 3** | **Inventory** | `inventory/` | Parts, part numbers, quantity, unit price, low-stock threshold |
| **Member 4** | **Customer Dashboard** | `dashboard/` | Customer overview, registered vehicles, bookings, active jobs |

---

## 🔀 Git Branching Strategy

To avoid merge conflicts on GitHub:

1. **Member 1 Branch:** `feature/customer-profile`
2. **Member 2 Branch:** `feature/job-card`
3. **Member 3 Branch:** `feature/inventory`
4. **Member 4 Branch:** `feature/customer-dashboard`

Each member works strictly within their own app directory:
- Member 1 modifies: `customers/`
- Member 2 modifies: `jobs/`
- Member 3 modifies: `inventory/`
- Member 4 modifies: `dashboard/`

---

## 🔗 How Teammates Connect to `Customer Profile`

### 1. Linking Job Cards to Customers & Vehicles (Teammate 2)
In `jobs/models.py`:
```python
from django.db import models

class JobCard(models.Model):
    job_number = models.CharField(max_length=20, unique=True) # e.g. "WB-1024"
    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        related_name='job_cards'
    )
    vehicle = models.ForeignKey(
        'customers.Vehicle',
        on_delete=models.CASCADE,
        related_name='job_cards'
    )
    complaint = models.TextField()
    status = models.CharField(
        max_length=30,
        choices=[
            ('Checked-in', 'Checked-in'),
            ('Diagnosis', 'Diagnosis'),
            ('Repairing', 'Repairing'),
            ('In Progress', 'In Progress'),
            ('Quality Check', 'Quality Check'),
            ('Completed', 'Completed'),
        ],
        default='Checked-in'
    )
    created_at = models.DateTimeField(auto_now_add=True)
```

> **Why this prevents conflicts:** Using string reference `'customers.Customer'` prevents circular import errors in Django and allows Django migrations to resolve dependencies automatically!

### 2. Linking Inventory / Parts to Job Cards (Teammate 3)
In `inventory/models.py`:
```python
from django.db import models

class InventoryItem(models.Model):
    name = models.CharField(max_length=150)
    part_number = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_stock_threshold = models.PositiveIntegerField(default=5)

class PartsUsage(models.Model):
    job_card = models.ForeignKey('jobs.JobCard', on_delete=models.CASCADE, related_name='parts_used')
    part = models.ForeignKey(InventoryItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
```

### 3. Customer Dashboard (Teammate 4)
In `dashboard/views.py`:
```python
from django.shortcuts import render
from customers.models import Customer, Vehicle

def customer_dashboard(request, customer_id=None):
    customer = Customer.objects.first() # or from request.user
    vehicles = customer.vehicles.all()
    # Query job cards if jobs app is merged:
    # active_jobs = customer.job_cards.exclude(status='Completed')
    ...
```

---

## ⚙️ Merging `settings.py` and `urls.py`

When teammates merge their branches into `main`:

### 1. In `workshop_os/settings.py`:
Simply uncomment their app in `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...
    'customers.apps.CustomersConfig',
    'jobs.apps.JobsConfig',           # <-- Uncomment when merging Member 2
    'inventory.apps.InventoryConfig', # <-- Uncomment when merging Member 3
    'dashboard.apps.DashboardConfig', # <-- Uncomment when merging Member 4
]
```

### 2. In `workshop_os/urls.py`:
Simply uncomment their URL routes:
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('customers:profile_default'), name='root'),
    path('customers/', include('customers.urls', namespace='customers')),
    path('jobs/', include('jobs.urls', namespace='jobs')),           # <-- Member 2
    path('inventory/', include('inventory.urls', namespace='inventory')), # <-- Member 3
    path('dashboard/', include('dashboard.urls', namespace='dashboard')), # <-- Member 4
]
```

---

## 🗄️ Database Migrations Protocol

To avoid migration conflicts:
1. Every team member runs `python manage.py makemigrations <their_app_name>`.
2. Do **not** run `makemigrations` without an app name (to keep migration files scoped to your app).
3. Once pulled into `main`, run:
   ```bash
   python manage.py migrate
   ```
4. To test with presentation data:
   ```bash
   python manage.py seed_customer
   ```
