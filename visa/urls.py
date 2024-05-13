from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="visa"),
    path("visa-details/<slug:slug>/", views.visa_details, name="visa_detail"),
    path('get-visa-types/', views.get_visa_types_for_country, name='get_visa_types'),
    path('get-visa-packages/', views.get_visa_packages_for_type, name='get_visa_packages'),

    path("booking-summary-of/<slug:slug>/", views.visa_booking_summary, name="get_visa_booking_summary"),
    path("<slug:slug>/booking/success/", views.visa_booking_process, name="visa_booking_success"),
    
]
