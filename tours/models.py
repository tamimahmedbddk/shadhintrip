from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class TourBanner(models.Model):
    image = models.ImageField(upload_to='background_images/', help_text=_("Upload a background image for the tour banner."))
    title = models.CharField(max_length=50, blank=True, null=True, help_text=_("Enter an optional title for the tour banner."))
    is_active = models.BooleanField(default=False, help_text=_("Activate this banner."))

    def __str__(self):
        return self.title or f"Background Image {self.id}"

class Country(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text=_("Enter the name of the country."))
    image = models.ImageField(upload_to='country_images/', help_text=_("Upload an image representing the country."))

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=200, help_text=_("Enter the name of the city."))
    country = models.ForeignKey(Country, related_name='cities', on_delete=models.CASCADE, help_text=_("Select the country this city belongs to."))

    def __str__(self):
        return f"{self.name}, {self.country}"

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text=_("Enter the name of the tour category, such as trekking, sightseeing, etc."))

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=200, help_text=_("Enter the name of the service."))
    icon_class = models.CharField(max_length=100, help_text=_("Enter the CSS class for the service icon."))

    def __str__(self):
        return self.name

class BaseTourEvent(models.Model):
    title = models.CharField(
        max_length=200,
        help_text=_("Enter the title of the tour or event. This will be displayed to users.")
    )
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    overview = RichTextField(help_text=_("Provide a brief overview of the tour or event."))
    description = RichTextField(help_text=_("Provide a detailed description of the tour or event."))
    activities = RichTextField(help_text=_("List the activities included in the tour or event."))
    includes = RichTextField(help_text=_("List what is included in the tour or event."))
    excludes = RichTextField(help_text=_("List what is not included in the tour or event."))
    requirements = RichTextField(help_text=_("Specify any requirements for participants."))
    rules = RichTextField(help_text=_("Specify any rules for the tour or event."))
    destinations = RichTextField(help_text=_("List the places or locations planned to be visited during the tour."))
    cancellation_policy = RichTextField(help_text=_("Describe the cancellation policy for the tour or event."))
    refund_policy = RichTextField(help_text=_("Describe the refund policy for the tour or event."))
    max_participants = models.PositiveIntegerField(
        default=1,
        help_text=_("Maximum number of participants allowed for the tour or event.")
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text=_("Enter the price for the tour or event."))
    category = models.ForeignKey(
        Category, related_name='%(class)ss', on_delete=models.CASCADE,
        help_text=_("Select the category for the tour or event.")
    )
    country = models.ForeignKey(
        Country, related_name='%(class)ss', on_delete=models.CASCADE,
        help_text=_("Select the country where the tour or event will take place.")
    )
    city = models.ForeignKey(
        City, related_name='%(class)ss', on_delete=models.CASCADE,
        help_text=_("Select the city where the tour or event will take place.")
    )
    duration_nights = models.PositiveIntegerField(help_text=_("Number of nights the tour or event will last."))
    duration_days = models.PositiveIntegerField(help_text=_("Number of days the tour or event will last."))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False, help_text=_("Check if the tour or event is featured."))
    is_active = models.BooleanField(default=True, help_text=_("Check if the tour or event is currently active."))
    services = models.ManyToManyField(
        Service, related_name='%(class)ss', blank=True,
        help_text=_("Select the services included in the tour or event.")
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tour_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

class Tour(BaseTourEvent):
    pass

class GroupEvent(BaseTourEvent):
    booking_policy = RichTextField(blank=True, verbose_name=_('Booking Policy'), help_text=_("Booking Policy"))
    advance_percentage = models.PositiveIntegerField(
        default=20,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text=_("Percentage of the total price required for confirmation.")
    )
    start_date = models.DateField(help_text=_("Start date of the group event."))
    end_date = models.DateField(help_text=_("End date of the group event."))

    def advance_required(self):
        return self.price * (self.advance_percentage / 100)

class TourItinerary(models.Model):
    tour = models.ForeignKey(Tour, related_name='itineraries', on_delete=models.CASCADE, null=True, blank=True)
    group_event = models.ForeignKey(GroupEvent, related_name='itineraries', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, help_text=_("Title of the itinerary item."))
    day = models.PositiveIntegerField(verbose_name=_('Day'), help_text=_("Day number in the itinerary."))
    description = RichTextField(verbose_name=_('Description'), help_text=_("Description of the itinerary item."))

    class Meta:
        verbose_name = _('Tour Itinerary')
        verbose_name_plural = _('Tour Itineraries')

    def __str__(self):
        return f"{self.tour.title if self.tour else self.group_event.title} - Day {self.day}: {self.title}"

class Image(models.Model):
    file = models.ImageField(upload_to='gallery/', help_text=_("Upload an image."))
    uploaded_at = models.DateTimeField(auto_now_add=True)
    caption = models.CharField(max_length=255, blank=True, help_text=_("Enter an optional caption for the image."))

    def __str__(self):
        return self.file.name

class TourImage(models.Model):
    tour = models.ForeignKey(Tour, related_name='images', on_delete=models.CASCADE)
    image = models.ForeignKey(Image, related_name='tour_images', on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False, help_text=_("Check if this is the main image for the tour."))

    def __str__(self):
        return f"Image for {self.tour.title} {'(Main)' if self.is_main else ''}"

class GroupEventImage(models.Model):
    group_event = models.ForeignKey(GroupEvent, related_name='images', on_delete=models.CASCADE)
    image = models.ForeignKey(Image, related_name='group_event_images', on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False, help_text=_("Check if this is the main image for the group event."))

    def __str__(self):
        return f"Image for {self.group_event.title} {'(Main)' if self.is_main else ''}"

class Video(models.Model):
    file = models.FileField(upload_to='videos/', help_text=_("Upload a video."))
    uploaded_at = models.DateTimeField(auto_now_add=True)
    caption = models.CharField(max_length=255, blank=True, help_text=_("Enter an optional caption for the video."))

    def __str__(self):
        return self.file.name

class TourVideo(models.Model):
    tour = models.ForeignKey(Tour, related_name='videos', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, related_name='tour_videos', on_delete=models.CASCADE)

    def __str__(self):
        return f"Video for {self.tour.title}"

class GroupEventVideo(models.Model):
    group_event = models.ForeignKey(GroupEvent, related_name='videos', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, related_name='group_event_videos', on_delete=models.CASCADE)

    def __str__(self):
        return f"Video for {self.group_event.title}"
