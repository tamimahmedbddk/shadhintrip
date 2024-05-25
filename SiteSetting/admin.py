from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Country,
    City,
    SiteConfiguration,
    Logo,
    Favicon,
    BackgroundImage,
    BackgroundVideo,
    SocialLink,
    ContactInfo,
)

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country__name')
    list_filter = ('country',)

class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'banner_image_preview', 'about_content_summary')
    search_fields = ('id',)
    readonly_fields = ('banner_image_preview', 'about_content_summary')
    fieldsets = (
        (None, {
            'fields': ('banner_image', 'banner_image_preview')
        }),
        ('Content', {
            'fields': ('about_content', 'about_content_summary', 'privacy_policy_content', 'terms_of_service', 'cancellation_policy', 'refund_policy', 'faq')
        }),
    )

    def banner_image_preview(self, obj):
        if obj.banner_image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.banner_image.url)
        return "No banner image"
    banner_image_preview.short_description = "Banner Image Preview"

    def about_content_summary(self, obj):
        if obj.about_content:
            return format_html('{}...', obj.about_content[:100])
        return "No content"
    about_content_summary.short_description = "About Content Summary"

class LogoAdmin(admin.ModelAdmin):
    list_display = ('id','image', 'is_active')
    search_fields = ('image',)
    list_filter = ('is_active',)

class FaviconAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'is_active')
    search_fields = ('image',)
    list_filter = ('is_active',)

class BackgroundImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('id',)

class BackgroundVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('id',)

class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'icon_class')
    list_filter = ('platform',)
    search_fields = ('platform', 'url')

class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'address')
    search_fields = ('phone', 'email', 'address')

admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(SiteConfiguration, SiteConfigurationAdmin)
admin.site.register(Logo, LogoAdmin)
admin.site.register(Favicon, FaviconAdmin)
admin.site.register(BackgroundImage, BackgroundImageAdmin)
admin.site.register(BackgroundVideo, BackgroundVideoAdmin)
admin.site.register(SocialLink, SocialLinkAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
