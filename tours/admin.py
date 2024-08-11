from django.contrib import admin
from .models import (
    TourBanner, Country, City, Category, Service,
    Tour, GroupEvent, TourItinerary, Image, Video, TourImage, GroupEventImage, TourVideo, GroupEventVideo, Place
)
from .forms import TourItineraryForm

class TourBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'title', 'is_active')
    search_fields = ('title',)
    list_filter = ('is_active',)

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    search_fields = ('name',)

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country__name')
    list_filter = ('country',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class')
    search_fields = ('name',)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class')
    search_fields = ('name',)

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'city')
    search_fields = ('name', 'city__name')
    list_filter = ('city',)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at', 'caption')
    search_fields = ('caption',)

class VideoAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at', 'caption')
    search_fields = ('caption',)

class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1

class GroupEventImageInline(admin.TabularInline):
    model = GroupEventImage
    extra = 1

class TourVideoInline(admin.TabularInline):
    model = TourVideo
    extra = 1

class GroupEventVideoInline(admin.TabularInline):
    model = GroupEventVideo
    extra = 1

class TourItineraryInline(admin.TabularInline):
    model = TourItinerary
    form = TourItineraryForm
    extra = 1
    fields = ('title', 'day', 'description')
    classes = ('collapse',)

class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'country', 'city', 'price', 'is_featured', 'is_active')
    search_fields = ('title', 'category__name', 'country__name', 'city__name')
    list_filter = ('category', 'country', 'city', 'is_featured', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['services', 'places']
    inlines = [TourItineraryInline, TourImageInline, TourVideoInline]

class GroupEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'country', 'city', 'price', 'advance_percentage', 'start_date', 'end_date', 'is_featured', 'is_active')
    search_fields = ('title', 'category__name', 'country__name', 'city__name')
    list_filter = ('category', 'country', 'city', 'is_featured', 'is_active', 'start_date', 'end_date')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['services', 'places']
    inlines = [TourItineraryInline, GroupEventImageInline, GroupEventVideoInline]

admin.site.register(TourBanner, TourBannerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Tour, TourAdmin)
admin.site.register(GroupEvent, GroupEventAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Video, VideoAdmin)