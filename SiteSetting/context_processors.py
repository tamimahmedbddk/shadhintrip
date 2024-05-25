from SiteSetting.models import BackgroundImage, BackgroundVideo, ContactInfo, SocialLink, SiteConfiguration,Logo,Favicon

def common_context(request):
    background_videos = BackgroundVideo.objects.filter(is_active=True).first()
    background_images = BackgroundImage.objects.filter(is_active=True).first()
    logo = Logo.objects.filter(is_active=True).first()
    site_settings = SiteConfiguration.objects.all()
    contact_info = ContactInfo.objects.all()
    social_links = SocialLink.objects.all()
    favicon = Favicon.objects.filter(is_active=True).first()

    return {
        'favicon':favicon,
        'logo':logo,
        'background_videos': background_videos,
        'banner': background_images,
        'site_settings': site_settings,
        'contact_info': contact_info,
        'social_links': social_links,
    }
