from django.shortcuts import render
from tours.models import Tour, Country, Category,GroupEvent
from visa.models import VisaPackage
from blog.models import Post

def index(request):
    popular_visa_packages = VisaPackage.objects.all()
    tours = list(Tour.objects.all()) + list(GroupEvent.objects.all())
    # countries = Country.objects.all()
    # categories = Category.objects.all()
    blog_posts = Post.objects.all().order_by('-id')[:3]

    context = {
        'popular_visa_packages': popular_visa_packages,
        'tours': tours,
        # 'countries': countries,
        # 'categories': categories,
        'blog_posts': blog_posts,
    }
    return render(request, 'index.html', context)

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
