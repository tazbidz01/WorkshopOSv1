from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    # Customer Profile View (UI 03)
    path('', views.customer_profile, name='profile_default'),
    path('<int:customer_id>/', views.customer_profile, name='profile'),

    # Directory & Search
    path('list/', views.customer_list, name='list'),

    # Actions
    path('<int:customer_id>/edit/', views.customer_edit, name='edit'),
    path('<int:customer_id>/add-note/', views.add_note, name='add_note'),

    # ==============================================================================
    # TENTATIVE / MODULAR: Add Vehicle Route
    # (Easy to disable: comment out this line when replacing with a dedicated vehicles module)
    # ==============================================================================
    path('<int:customer_id>/add-vehicle/', views.add_vehicle, name='add_vehicle'),
    # ==============================================================================
    # END TENTATIVE / MODULAR: Add Vehicle Route
    # ==============================================================================

    # ==============================================================================
    # TENTATIVE: Create Job Card Route
    # (Easy to disable: comment out this line when merging Member 2's 'jobs' app)
    # ==============================================================================
    path('<int:customer_id>/create-job-card/', views.create_job_card, name='create_job_card'),
    # ==============================================================================
    # END TENTATIVE: Create Job Card Route
    # ==============================================================================
]
