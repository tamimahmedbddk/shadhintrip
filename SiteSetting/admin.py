from django.contrib import admin
from .models import SiteSettings, BackgroundImage, SocialLink, ContactInfo

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name']
    fieldsets = (
        (None, {
            'fields': ('site_name', 'logo', 'favicon',)
        }),
        ('Content', {
            'fields': ('about_content', 'privacy_policy_content','terms_of_service','cancellation_policy','refund_policy','faq',)
        }),
    )

@admin.register(BackgroundImage)
class BackgroundImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'is_active']
    list_filter = ['is_active']
    search_fields = ['id']

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url']
    list_filter = ['platform']
    search_fields = ['platform']

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email', 'address']
