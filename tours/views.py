from django.shortcuts import get_object_or_404, render, redirect
from .models import Tour, Category, Country, City, TourBanner, GroupEvent
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from visa.models import VisaPackage
from bookings.models import TourBooking
from django.db import IntegrityError

def list_tours(request):
    popular_visa_packages = VisaPackage.objects.all()
    tours = list(Tour.objects.all()) + list(GroupEvent.objects.all())
    categories = Category.objects.all()
    countries = Country.objects.all()
    cities = City.objects.all()
    banner = TourBanner.objects.filter(is_active=True).first()

    category_id = request.GET.get('category')
    country_id = request.GET.get('country')
    city_id = request.GET.get('city')
    place = request.GET.get('place')

    selected_category = None
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)

    if category_id:
        tours = [tour for tour in tours if tour.category_id == int(category_id)]
    if country_id:
        tours = [tour for tour in tours if tour.country_id == int(country_id)]
    if city_id:
        tours = [tour for tour in tours if tour.city_id == int(city_id)]
    if place:
        tours = [tour for tour in tours if place.lower() in tour.destinations.lower()]

    context = {
        'popular_visa_packages': popular_visa_packages,
        'banner': banner,
        'tours': tours,
        'categories': categories,
        'countries': countries,
        'cities': cities,
        'selected_category': selected_category,
    }
    return render(request, 'tours/home.html', context)


def tour_detail(request, slug):
    # Try to find a Tour or GroupEvent with the given slug
    try:
        tour_details = Tour.objects.get(slug=slug)
        other_tours = Tour.objects.exclude(slug=slug)
        is_tour = True
    except Tour.DoesNotExist:
        tour_details = get_object_or_404(GroupEvent, slug=slug)
        other_tours = GroupEvent.objects.exclude(slug=slug)
        is_tour = False

    context = {
        'tour_details': tour_details,
        'other_tours': other_tours,
    }
    return render(request, 'tours/tour_details.html', context)




@login_required(login_url='login')
def booking_summary(request, slug):
    try:
        tour_details = Tour.objects.get(slug=slug)
        main_image = tour_details.images.filter(is_main=True).first()
    except Tour.DoesNotExist:
        tour_details = get_object_or_404(GroupEvent, slug=slug)
        main_image = tour_details.images.filter(is_main=True).first()

    context = {
        'tour_details': tour_details,
        'main_image': main_image,
    }
    return render(request, 'tours/booking_summary.html', context)





@login_required(login_url='login')
def booking_success(request, slug):
    tour = None
    group_event = None

    try:
        tour = Tour.objects.get(slug=slug)
    except Tour.DoesNotExist:
        group_event = get_object_or_404(GroupEvent, slug=slug)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        nationality = request.POST.get('nationality')
        date = request.POST.get('date')
        address = request.POST.get('address')

        if not (first_name and last_name and phone_number and nationality and date and address):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('booking_summary', slug=slug)

        num_travelers = int(request.POST.get('num_travelers', 1))
        total_price = (tour.price if tour else group_event.price) * num_travelers

        try:
            booking = TourBooking.objects.create(
                user=request.user,
                tour=tour if tour else None,
                group_event=group_event if group_event else None,
                quantity=num_travelers,
                total_price=total_price,
            )
        except IntegrityError:
            messages.error(request, 'You have already made a booking for this tour/event. For modifications or any other assistance, please contact support.')
            return redirect('booking_summary', slug=slug)

        context = {
            'tour_details': tour or group_event,
        }
        return render(request, 'tours/booking_success.html', context)

    return redirect('index')