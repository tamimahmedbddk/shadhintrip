from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _


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


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, blank=True, null=True, help_text=_("Enter the name of the site."))
    logo = models.ImageField(upload_to='logos/', blank=True, null=True, help_text=_("Upload the main logo for the site."))
    favicon = models.ImageField(upload_to='favicons/', blank=True, null=True, help_text=_("Upload the favicon for the site."))
    about_content = RichTextField(blank=True, null=True, help_text=_("Content for the about page."))
    privacy_policy_content = RichTextField(blank=True, null=True, help_text=_("Content for the privacy policy page."))
    terms_of_service = RichTextField(blank=True, null=True, help_text=_("Content for the terms of service page."))
    cancellation_policy = RichTextField(blank=True, null=True, help_text=_("Content for the cancellation policy page."))
    refund_policy = RichTextField(blank=True, null=True, help_text=_("Content for the refund policy page."))
    faq = RichTextField(blank=True, null=True, help_text=_("Content for the FAQ page."))

    def __str__(self):
        return self.site_name or "Site Settings"

class BackgroundImage(models.Model):
    image = models.ImageField(upload_to='background_images/', help_text=_("Upload a background image."))
    is_active = models.BooleanField(default=True, help_text=_("Activate this background image."))

    def __str__(self):
        return f"Background Image {self.id}"

class BackgroundVideo(models.Model):
    video = models.FileField(upload_to='background_videos/', help_text=_("Upload a background video."))
    is_active = models.BooleanField(default=True, help_text=_("Activate this background video."))

    def __str__(self):
        return f"Background Video {self.id}"


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        # Add more platforms as needed
    ]

    PLATFORM_ICON_CLASSES = {
        'facebook': 'icon-facebook',
        'twitter': 'icon-twitter',
        'instagram': 'icon-instagram',
        'linkedin': 'icon-linkedin',
        'youtube': 'fa fa-youtube',
        # Add more mappings as needed
    }

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, help_text=_("Select the social media platform."))
    url = models.URLField(help_text=_("Enter the URL for the social media profile."))
    icon_class = models.CharField(max_length=100, blank=True, help_text=_("Class name for the icon."))

    def __str__(self):
        return f"{self.get_platform_display()}"

    def save(self, *args, **kwargs):
        if not self.icon_class:
            self.icon_class = self.PLATFORM_ICON_CLASSES.get(self.platform, '')
        super().save(*args, **kwargs)


class ContactInfo(models.Model):
    phone = models.CharField(max_length=20, help_text=_("Enter the contact phone number."))
    email = models.EmailField(help_text=_("Enter the contact email address."))
    address = models.TextField(help_text=_("Enter the contact address."))

    def __str__(self):
        return "Contact Information"
