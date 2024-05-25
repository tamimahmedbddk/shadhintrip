from django.contrib import admin
from .models import SiteSettings, BackgroundImage, BackgroundVideo, SocialLink, ContactInfo

class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name',)
    search_fields = ('site_name',)
    fieldsets = (
        (None, {
            'fields': ('site_name', 'logo', 'favicon')
        }),
        ('Content', {
            'fields': ('about_content', 'privacy_policy_content', 'terms_of_service', 'cancellation_policy', 'refund_policy', 'faq')
        }),
    )

class BackgroundImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('id',)

class BackgroundVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('id',)

class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url','icon_class')
    list_filter = ('platform',)
    search_fields = ('platform', 'url')

class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email')
    search_fields = ('phone', 'email', 'address')

admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(BackgroundImage, BackgroundImageAdmin)
admin.site.register(BackgroundVideo, BackgroundVideoAdmin)
admin.site.register(SocialLink, SocialLinkAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
