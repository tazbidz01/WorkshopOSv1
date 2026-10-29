"""
URL configuration for WorkshopOS project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    # Default root redirects to Customer Profile (Current Module)
    path('', lambda request: redirect('customers:profile_default'), name='root'),

    # Component 1 (Current): Customer Profile
    path('customers/', include('customers.urls', namespace='customers')),

    # ==========================================================
    # Teammate Components (Uncomment when merged)
    # ==========================================================
    # Component 2: Job Card (Teammate 2)
    # path('jobs/', include('jobs.urls', namespace='jobs')),

    # Component 3: Inventory (Teammate 3)
    # path('inventory/', include('inventory.urls', namespace='inventory')),

    # Component 4: Customer Dashboard (Teammate 4)
    # path('dashboard/', include('dashboard.urls', namespace='dashboard')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
