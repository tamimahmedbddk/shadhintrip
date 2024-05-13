from django.shortcuts import get_object_or_404, render, redirect
from .models import Tour, Category, Country, City, TourBanner
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from visa.models import VisaPackage
from bookings.models import TourBooking

def list_tours(request):
    # visa=======
    popular_visa_packages = VisaPackage.objects.all()
    # tour=======
    tours = Tour.objects.all().order_by('-id')
    categories = Category.objects.all()
    countries = Country.objects.all()
    cities = City.objects.all()
    banner = TourBanner.objects.all().first()

    # Filter tours based on form submission
    category_id = request.GET.get('category')
    country_id = request.GET.get('country')
    city_id = request.GET.get('city')
    place = request.GET.get('place')

    # Get selected category details
    selected_category = None
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)

    if category_id:
        tours = tours.filter(category_id=category_id)
    if country_id:
        tours = tours.filter(country_id=country_id)
    if city_id:
        tours = tours.filter(city_id=city_id)
    if place:
        tours = tours.filter(planned_destinations__icontains=place)

    context = {
        'popular_visa_packages':popular_visa_packages,
        'banner': banner,
        'tours': tours,
        'categories': categories,
        'countries': countries,
        'cities': cities,
        'selected_category': selected_category,  # Pass selected category to template
    }
    return render(request, 'tours/home.html', context)

def tour_detail(request, slug):
    # Retrieve the current tour package
    tour_details = get_object_or_404(Tour, slug=slug)

    # Retrieve other tour packages excluding the current one
    other_tours = Tour.objects.exclude(slug=slug)

    context = {
        'tour_details': tour_details,
        'other_tours': other_tours,
    }
    return render(request, 'tours/tour_details.html', context)


@login_required(login_url='login')
def booking_summary(request, slug):
    tour_details =  get_object_or_404(Tour, slug=slug)
    
    context = {
        'tour_details': tour_details,

    }
    return render(request, 'tours/booking_summary.html', context)


def booking_success(request, slug):
    tour = get_object_or_404(Tour, slug=slug)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        nationality = request.POST.get('nationality')
        date = request.POST.get('date')
        address = request.POST.get('address')

        # Check if all required fields are provided
        if not (first_name and last_name and phone_number,nationality,date,address):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('booking_summary', slug=slug)

        # Get number of travelers (default to 1 if not provided)
        num_travelers = int(request.POST.get('num_travelers', 1))
        print(num_travelers)

        # Calculate total price based on the number of travelers
        total_price = tour.price * num_travelers

        # Create the booking object and save it to the database
        booking = TourBooking.objects.create(
            tour=tour,
            user=request.user,
            quantity=num_travelers,
            total_price=total_price,
            # first_name=first_name,
            # last_name=last_name,
            # phone_number=phone_number,
            # Add other fields as needed
        )
        return render(request, 'tours/booking_success.html')
    return render(request, 'tours/booking_summary.html')
