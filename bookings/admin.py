from django.contrib import admin
from .models import TourBooking, VisaBooking

class TourBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tour','group_event','quantity', 'total_price', 'booking_date', 'status', 'is_confirmed', 'is_paid')
    list_filter = ('tour', 'group_event', 'user', 'booking_date', 'status', 'is_confirmed', 'is_paid')
    search_fields = ('user__email', 'tour__title')
    readonly_fields = ('booking_date',)

class VisaBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'visa_package', 'quantity', 'total_price', 'booking_date', 'status', 'is_confirmed', 'is_paid')
    list_filter = ('visa_package', 'user', 'booking_date', 'status', 'is_confirmed', 'is_paid')
    search_fields = ('user__email', 'visa_package__title')
    readonly_fields = ('booking_date',)

admin.site.register(TourBooking, TourBookingAdmin)
admin.site.register(VisaBooking, VisaBookingAdmin)
