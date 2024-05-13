from django.urls import path

from . import views

urlpatterns = [
    # path("", views.list_tours, name="tour"),
    path('booking_history/', views.booking_history, name='booking_history'),
    
]
