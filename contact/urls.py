from django.urls import path
from .views import contact_us, contact_success

urlpatterns = [
    path('', contact_us, name='contact_us'),
    path('success/', contact_success, name='contact_success'),
]
