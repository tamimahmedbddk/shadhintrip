from django.shortcuts import render
from django.http import HttpResponse
from tours.models import Tour, Country, Category
from visa.models import VisaPackage
from blog.models import Post
from SiteSetting.models import BackgroundImage,BackgroundVideo, ContactInfo, SocialLink, SiteSettings

def get_common_context():
    background_videos = BackgroundVideo.objects.all()
    background_images = BackgroundImage.objects.all()
    site_settings = SiteSettings.objects.all()
    contact_info = ContactInfo.objects.all()
    social_links = SocialLink.objects.all()

    return {
        'background_videos':background_videos,
        'background_images': background_images,
        'site_settings': site_settings,
        'contact_info': contact_info,
        'social_links': social_links,
    }

def index(request):
    # visa_offers = VisaPackage.objects.all()[:3]
    popular_visa_packages = VisaPackage.objects.all()
    tours = Tour.objects.all().order_by('-id')[:6]
    Popular_Tour_Packages = Tour.objects.all().order_by('id')[:6]
    countries = Country.objects.all()
    categories = Category.objects.all()
    blog_posts = Post.objects.all().order_by('-id')[:3]

    context = {
        # 'visa_offers': visa_offers,
        'popular_visa_packages': popular_visa_packages,
        'tours': tours,
        'countries': countries,
        'categories': categories,
        'blog_posts': blog_posts,
        'Popular_Tour_Packages':Popular_Tour_Packages,
    }
    context.update(get_common_context())
    return render(request, 'index.html', context)

def common_page_view(request, template_name):
    context = get_common_context()
    return render(request, template_name, context)

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
