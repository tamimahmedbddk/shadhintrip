from SiteSetting.models import BackgroundImage, BackgroundVideo, ContactInfo, SocialLink, SiteSettings

def common_context(request):
    background_videos = BackgroundVideo.objects.all()
    background_images = BackgroundImage.objects.filter(is_active=True).first()
    site_settings = SiteSettings.objects.all()
    contact_info = ContactInfo.objects.all()
    social_links = SocialLink.objects.all()

    return {
        'background_videos': background_videos,
        'banner': background_images,
        'site_settings': site_settings,
        'contact_info': contact_info,
        'social_links': social_links,
    }
