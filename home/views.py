from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db import models
from tours.models import Tour, GroupEvent, Category
from visa.models import VisaPackage, VisaType
from SiteSetting.models import Country
from blog.models import Post

def index(request):
    popular_visa_packages = VisaPackage.objects.all()
    tours = list(Tour.objects.all()) + list(GroupEvent.objects.all())
    blog_posts = Post.objects.all().order_by('-id')[:3]

    context = {
        'popular_visa_packages': popular_visa_packages,
        'tours': tours,
        'blog_posts': blog_posts,
    }
    return render(request, 'index.html', context)

def get_tour_countries(request):
    countries = Country.objects.filter(
        models.Q(tours__isnull=False) | models.Q(groupevents__isnull=False)
    ).distinct()
    countries_data = [
        {'id': country.id, 'name': country.name, 'image': country.image.url if country.image else ''}
        for country in countries
    ]
    return JsonResponse(countries_data, safe=False)

def get_tour_categories(request):
    country_id = request.GET.get('country_id')
    country = get_object_or_404(Country, id=country_id)
    categories = Category.objects.filter(
        models.Q(tours__country=country) | models.Q(groupevents__country=country)
    ).distinct()
    data = [{'country_id': country.id,'category_id': category.id, 'name': category.name, 'icon':category.icon_class} for category in categories]
    return JsonResponse(data, safe=False)

def get_tour_packages(request):
    country_id = request.GET.get('country_id')
    category_id = request.GET.get('category_id')
    tours = list(Tour.objects.filter(country_id=country_id, category_id=category_id)) + list(GroupEvent.objects.filter(country_id=country_id, category_id=category_id))

    data = [
        {
            'id': tour.id,
            'title': tour.title,
            'image': tour.images.first().image.file.url if tour.images.exists() else '',
        } for tour in tours
    ]
    return JsonResponse(data, safe=False)

def get_visa_countries(request):
    countries = Country.objects.filter(visa_packages__isnull=False).distinct()
    data = [{'id': country.id, 'name': country.name, 'image': country.image.url} for country in countries]
    return JsonResponse(data, safe=False)

def get_visa_types(request):
    country_id = request.GET.get('country_id')
    visa_types = VisaType.objects.filter(country_id=country_id).distinct()
    data = [{'id': visa_type.id, 'name': visa_type.name} for visa_type in visa_types]
    return JsonResponse(data, safe=False)

def get_visa_packages(request):
    country_id = request.GET.get('country_id')
    visa_type_id = request.GET.get('visa_type_id')
    visas = VisaPackage.objects.filter(country_id=country_id, visa_type_id=visa_type_id)
    data = [{'id': visa.id, 'title': visa.title, 'image': visa.image.url} for visa in visas]
    return JsonResponse(data, safe=False)

def common_page_view(request, template_name):
    return render(request, template_name)

def about_us(request):
    return common_page_view(request, 'site_settings/about-us.html')

def privacy_policy(request):
    return common_page_view(request, 'site_settings/privacy-policy.html')

def terms_of_service(request):
    return common_page_view(request, 'site_settings/terms.html')

def cancellation_policy(request):
    return common_page_view(request, 'site_settings/cancellation_policy.html')

def refund_policy(request):
    return common_page_view(request, 'site_settings/refund-policy.html')

def faq(request):
    return common_page_view(request, 'site_settings/faq.html')
