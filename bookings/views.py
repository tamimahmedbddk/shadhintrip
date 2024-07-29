from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from.models import VisaBooking,TourBooking
from django.core.paginator import Paginator

from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='login')
def booking_history(request):
    visa_bookings = VisaBooking.objects.all().filter(user=request.user).order_by('-id')
    visa_bookings_paginator = Paginator(visa_bookings, 10)  # Show 10 visa packages per page
    page_number = request.GET.get('page')
    visa_booking_page_obj = visa_bookings_paginator.get_page(page_number)


    tour_bookings = TourBooking.objects.all().filter(user=request.user).order_by('-id')
    tour_bookings_paginator = Paginator(tour_bookings, 10)  # Show 10 visa packages per page
    page_number = request.GET.get('page')
    tour_booking_page_obj = tour_bookings_paginator.get_page(page_number)

    context = {
        'visa_bookings': visa_booking_page_obj,  # Pass the paginated bookings
        'visa_booking_page_obj': visa_booking_page_obj,  # Pass the page object for pagination controls


        'tour_bookings':tour_booking_page_obj,
        'tour_booking_page_obj': tour_booking_page_obj,
    }
    return render(request, 'bookings/booking-history.html', context)