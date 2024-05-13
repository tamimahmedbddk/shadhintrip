from django.contrib import admin
from .models import Tour, TourImage, Service, Country, City, TourItinerary, Category, TourBanner

class TourItineraryInline(admin.StackedInline):
    model = TourItinerary
    extra = 1

class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    inlines = [TourItineraryInline, TourImageInline]
    list_display = ['title', 'category', 'country', 'city', 'is_featured', 'is_active']
    list_filter = ['category', 'country', 'city', 'is_featured', 'is_active']
    search_fields = ['title', 'category__name', 'country__name', 'city__name', 'overview', 'description']
    filter_horizontal = ['services']
    fieldsets = [
        ('Basic Information', {'fields': ['title', 'slug', 'overview', 'description']}),
        ('Additional Information', {'fields': ['activities', 'includes', 'excludes', 'requirements', 'tour_rules', 'planned_destinations', 'cancellation_policy']}),
        ('Booking Details', {'fields': ['max_participants', 'price']}),
        ('Location Details', {'fields': ['category', 'country', 'city']}),
        ('Duration Details', {'fields': ['duration_nights', 'duration_days']}),
        ('Status', {'fields': ['is_featured', 'is_active']}),
        ('Services', {'fields': ['services']}),
    ]
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_class']

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(TourBanner)
class TourBannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'title', 'is_active']
