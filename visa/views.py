from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import VisaPackage, VisaBanner, Country, VisaType, VisaPackage
from django.http import JsonResponse
from django.contrib import messages
from bookings.models import VisaBooking
from tours.models import Tour
from django.core.paginator import Paginator

def index(request):
    banner = VisaBanner.objects.filter(is_active=True).first()
    countries = Country.objects.all().order_by('-id')
    visa_types = VisaType.objects.all()
    popular_visa_packages = VisaPackage.objects.all()  # for banner, we should fix this later
    tours = Tour.objects.all().order_by('-id')  # for banner, we should fix this later

    # Pagination for visa packages
    visa_packages_list = VisaPackage.objects.all()
    paginator = Paginator(visa_packages_list, 12)  # Show 10 visa packages per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'countries': countries,
        'visa_packages': page_obj,  # Pass the paginated visa packages
        'banner': banner,
        'visa_types': visa_types,
        'popular_visa_packages': popular_visa_packages,
        'tours': tours,
        'page_obj': page_obj,  # Pass the page object for pagination controls
    }

    return render(request, 'visa/index.html', context)


def visa_details(request, slug):
    visa_details = get_object_or_404(VisaPackage, slug=slug)
    
    if visa_details.image:
        image_url = request.build_absolute_uri(visa_details.image.url)
    else:
        image_url = request.build_absolute_uri(static('assets/img/tour/card/1.png'))
    
    context = {
        'visa_details': visa_details,
        'image_url': image_url,  # Add this to the context
    }
    return render(request, 'visa/visa-details.html', context)



def get_visa_types_for_country(request):
    country_name = request.GET.get('country', '')
    
    if country_name:
        visa_types = VisaType.objects.filter(country__name=country_name).values('id', 'name')
        visa_types_data = list(visa_types)
        return JsonResponse(visa_types_data, safe=False)
    else:
        return JsonResponse({'error': 'No country selected'}, status=400)



def get_visa_packages_for_type(request):
    visa_type_id = request.GET.get('visa_type', '').strip()
    
    if not visa_type_id:
        return JsonResponse({'error': 'Select a visa type.'}, status=400)

    try:
        visa_packages = VisaPackage.objects.filter(visa_type__id=visa_type_id).values('id', 'title')
        
        if not visa_packages:
            return JsonResponse({'message': 'No visa packages found for this type.'}, status=404)
        
        return JsonResponse(list(visa_packages), safe=False)
    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)


@login_required(login_url='login')
def visa_booking_summary(request, slug):
    visa_package =  get_object_or_404(VisaPackage, slug=slug)
    
    context = {
        'visa_package': visa_package,

    }
    return render(request, 'visa/visa_booking_summary.html', context)

def visa_booking_process(request, slug):
    visa_package = get_object_or_404(VisaPackage, slug=slug)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        nationality = request.POST.get('nationality')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')

        # Check if all required fields are provided
        if not (first_name and last_name and phone_number,nationality,date_of_birth,address):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('visa_booking_summary', slug=slug)

        # Get number of travelers (default to 1 if not provided)
        num_applicants = int(request.POST.get('num_applicants', 1))

        # Calculate total price based on the number of travelers
        total_price = visa_package.total_fee * num_applicants

        # Create the booking object and save it to the database
        visa_booking = VisaBooking.objects.create(
            visa_package=visa_package,
            user=request.user,
            quantity=num_applicants,
            total_price=total_price,
        )
        context = {
        'visa_package': visa_package,

        }
        return render(request, 'visa/booking-success.html', context)
    return redirect('index')
