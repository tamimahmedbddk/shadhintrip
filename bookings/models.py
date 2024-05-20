from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from tours.models import Tour,GroupEvent
from visa.models import VisaPackage
from django.core.exceptions import ValidationError

User = get_user_model()

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
]

PAYMENT_METHOD_CHOICES = [
    ('online', 'Online Payment'),
    ('cash', 'Cash on Delivery'),
    ('bank_transfer', 'Bank Transfer'),
]



class TourBooking(models.Model):
    user = models.ForeignKey(User, related_name='tour_bookings', on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True, blank=True)
    group_event = models.ForeignKey(GroupEvent, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    confirmation_date = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='online')
    payment_reference = models.CharField(max_length=100, blank=True)
    payment_received_by = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name_plural = "Tour Bookings"
        constraints = [
            models.UniqueConstraint(fields=['user', 'tour'], name='unique_tour_booking'),
            models.UniqueConstraint(fields=['user', 'group_event'], name='unique_group_event_booking'),
        ]

    def clean(self):
        if self.tour and self.group_event:
            raise ValidationError("Cannot select both tour and group event. Please select only one.")
        if not self.tour and not self.group_event:
            raise ValidationError("Please select either a tour or a group event.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.tour.title if self.tour else self.group_event.title} - {self.booking_date}"



class VisaBooking(models.Model):
    visa_package = models.ForeignKey(VisaPackage, related_name='bookings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='visa_bookings', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    confirmation_date = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='online')
    payment_reference = models.CharField(max_length=100, blank=True)
    payment_received_by = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name_plural = "Visa Bookings"

    def __str__(self):
        return f"{self.user.email} - {self.visa_package.title} - {self.booking_date}"
