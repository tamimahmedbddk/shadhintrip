from django.urls import path

from . import views


urlpatterns = [
    path("", views.list_tours, name="tour"),
    path("tour-details/<slug:slug>/", views.tour_detail, name="tour_detail"),
    path("booking-summary-of/<slug:slug>/", views.booking_summary, name="booking_summary"),
    path("<slug:slug>/booking/success/", views.booking_success, name="booking_success"),
]
