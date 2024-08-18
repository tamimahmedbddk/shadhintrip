from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from io import BytesIO
from django.core.files.base import ContentFile
import os
from PIL import Image

class Country(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text=_("Enter the name of the country."))
    image = models.ImageField(upload_to='site_images/country_images/', help_text=_("Upload an image representing the country."))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self._compress_image(self.image, (800, 600))  # Adjust size as needed

    def _compress_image(self, image_field, size):
        original_path = image_field.path
        image = Image.open(image_field)
        image = image.resize(size, Image.Resampling.LANCZOS)
        im_io = BytesIO()
        image.save(im_io, format='JPEG', quality=85)
        new_image = ContentFile(im_io.getvalue(), name=os.path.basename(original_path))

        if os.path.exists(original_path):
            os.remove(original_path)

        image_field.save(os.path.basename(original_path), new_image, save=False)

class City(models.Model):
    name = models.CharField(max_length=200, help_text=_("Enter the name of the city."))
    country = models.ForeignKey(Country, related_name='cities', on_delete=models.CASCADE, help_text=_("Select the country this city belongs to."))

    def __str__(self):
        return f"{self.name}, {self.country}"

class SiteConfiguration(models.Model):
    banner_image = models.ImageField(upload_to='site_images/main_banner/', blank=True, null=True, help_text=_("Upload the banner image for the site."))
    about_content = RichTextField(blank=True, null=True, help_text=_("Content for the about page."))
    privacy_policy_content = RichTextField(blank=True, null=True, help_text=_("Content for the privacy policy page."))
    terms_of_service = RichTextField(blank=True, null=True, help_text=_("Content for the terms of service page."))
    cancellation_policy = RichTextField(blank=True, null=True, help_text=_("Content for the cancellation policy page."))
    refund_policy = RichTextField(blank=True, null=True, help_text=_("Content for the refund policy page."))
    faq = RichTextField(blank=True, null=True, help_text=_("Content for the FAQ page."))

    def __str__(self):
        return "Site Configuration"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.banner_image:
            self._compress_image(self.banner_image, (1920, 1080))  # Adjust size as needed

    def _compress_image(self, image_field, size):
        original_path = image_field.path
        image = Image.open(image_field)
        image = image.resize(size, Image.Resampling.LANCZOS)
        im_io = BytesIO()
        image.save(im_io, format='JPEG', quality=85)
        new_image = ContentFile(im_io.getvalue(), name=os.path.basename(original_path))

        if os.path.exists(original_path):
            os.remove(original_path)

        image_field.save(os.path.basename(original_path), new_image, save=False)

class Logo(models.Model):
    image = models.ImageField(upload_to='site_images/logo/', help_text=_("Upload the main logo for the site."))
    is_active = models.BooleanField(default=True, help_text=_("Activate this logo."))

    def __str__(self):
        return f"Logo {self.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self._compress_image(self.image, (300, 300))  # Adjust size as needed

    def _compress_image(self, image_field, size):
        original_path = image_field.path
        image = Image.open(image_field)
        image = image.resize(size, Image.Resampling.LANCZOS)
        im_io = BytesIO()
        image.save(im_io, format='JPEG', quality=85)
        new_image = ContentFile(im_io.getvalue(), name=os.path.basename(original_path))

        if os.path.exists(original_path):
            os.remove(original_path)

        image_field.save(os.path.basename(original_path), new_image, save=False)

class Favicon(models.Model):
    image = models.ImageField(upload_to='site_images/favicons/', help_text=_("Upload the favicon for the site."))
    is_active = models.BooleanField(default=True, help_text=_("Activate this favicon."))

    def __str__(self):
        return f"Favicon {self.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self._compress_image(self.image, (64, 64))  # Adjust size as needed

    def _compress_image(self, image_field, size):
        original_path = image_field.path
        image = Image.open(image_field)
        image = image.resize(size, Image.Resampling.LANCZOS)
        im_io = BytesIO()
        image.save(im_io, format='PNG', quality=95)  # PNG is more suitable for icons
        new_image = ContentFile(im_io.getvalue(), name=os.path.basename(original_path))

        if os.path.exists(original_path):
            os.remove(original_path)

        image_field.save(os.path.basename(original_path), new_image, save=False)

class BackgroundImage(models.Model):
    image = models.ImageField(upload_to='site_images/main_banner/', help_text=_("Upload a background image."))
    is_active = models.BooleanField(default=True, help_text=_("Activate this background image."))

    def __str__(self):
        return f"Background Image {self.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self._compress_image(self.image, (1920, 1080))  # Adjust size as needed

    def _compress_image(self, image_field, size):
        original_path = image_field.path
        image = Image.open(image_field)
        image = image.resize(size, Image.Resampling.LANCZOS)
        im_io = BytesIO()
        image.save(im_io, format='JPEG', quality=85)
        new_image = ContentFile(im_io.getvalue(), name=os.path.basename(original_path))

        if os.path.exists(original_path):
            os.remove(original_path)

        image_field.save(os.path.basename(original_path), new_image, save=False)

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
