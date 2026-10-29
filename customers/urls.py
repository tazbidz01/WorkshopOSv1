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
    path('<int:customer_id>/add-vehicle/', views.add_vehicle, name='add_vehicle'),
    path('<int:customer_id>/add-note/', views.add_note, name='add_note'),
]
