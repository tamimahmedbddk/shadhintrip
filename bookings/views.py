from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from.models import VisaBooking,TourBooking

from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='login')
def booking_history(request):
    visa_bookings = VisaBooking.objects.all().filter(user=request.user).order_by('-id')
    tour_bookings = TourBooking.objects.all().filter(user=request.user).order_by('-id')
    context = {
        'bookings': visa_bookings,
        'tour_bookings':tour_bookings,
    }
    return render(request, 'bookings/booking-history.html', context)