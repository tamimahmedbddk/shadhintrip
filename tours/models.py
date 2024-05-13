from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()

class TourBanner(models.Model):
    """
    Model to store background images.
    """
    image = models.ImageField(upload_to='background_images/')
    title = models.CharField(max_length=50, blank=True,null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Background Image {self.id}"

def validate_unique_name(value):
    if Country.objects.filter(name=value).exists():
        raise ValidationError('A country with this name already exists.')

class Country(models.Model):
    name = models.CharField(max_length=200, validators=[validate_unique_name])
    image = models.ImageField(upload_to='country_images/')

    def __str__(self):
        return self.name

def validate_unique_city_name(value, country):
    if City.objects.filter(name=value, country=country).exists():
        raise ValidationError('A city with this name in the specified country already exists.')

class City(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, related_name='cities', on_delete=models.CASCADE)

    def clean(self):
        validate_unique_city_name(self.name, self.country)

    def __str__(self):
        return f"{self.name}, {self.country}"

def validate_unique_category_name(value):
    if Category.objects.filter(name=value).exists():
        raise ValidationError('A category with this name already exists.')

class Category(models.Model):
    name = models.CharField(max_length=200, validators=[validate_unique_category_name])
    description = RichTextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=200)
    icon_class = models.CharField(max_length=100)  # Assuming input for class name

    def __str__(self):
        return self.name

class Tour(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = RichTextField()
    description = RichTextField()
    activities = RichTextField()
    includes = RichTextField()
    excludes = RichTextField()
    requirements = RichTextField()
    tour_rules = RichTextField()
    planned_destinations = models.TextField(blank=True, help_text="Places or locations planned to be visited during the tour")
    cancellation_policy = RichTextField()
    max_participants = models.PositiveIntegerField(default=1, help_text=_("Maximum number of participants"))
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='tours', on_delete=models.CASCADE)
    country = models.ForeignKey(Country, related_name='tours', on_delete=models.CASCADE)
    city = models.ForeignKey(City, related_name='tours', on_delete=models.CASCADE)
    duration_nights = models.PositiveIntegerField(help_text=_("Number of nights"))
    duration_days = models.PositiveIntegerField(help_text=_("Number of days"))
    created_at = models.DateTimeField(auto_now_add=True)  # Added package creation date
    edited_at = models.DateTimeField(auto_now=True)  # Added edit date
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    services = models.ManyToManyField(Service, related_name='tours', blank=True)
    itinerary = models.ManyToManyField('self', symmetrical=False, through='TourItinerary', related_name='related_itineraries', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tour_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

class TourItinerary(models.Model):
    tour = models.ForeignKey(Tour, related_name='tour_itineraries', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    day = models.PositiveIntegerField(verbose_name=_('Day'))
    description = RichTextField(verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Tour Itinerary')
        verbose_name_plural = _('Tour Itineraries')

    def __str__(self):
        return f"{self.tour.title} - Day {self.day}: {self.title}"

class TourImage(models.Model):
    tour = models.ForeignKey(Tour, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tours/images/')
    is_main = models.BooleanField(default=False)
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.tour.title} {'(Main)' if self.is_main else ''}"
