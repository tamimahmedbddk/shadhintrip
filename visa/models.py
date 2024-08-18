from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from SiteSetting.models import Country

from io import BytesIO
from django.core.files.base import ContentFile
import os
from PIL import Image as PILImage  # Alias the PIL Image class to avoid conflicts

User = get_user_model()

class VisaBanner(models.Model):
    image = models.ImageField(upload_to='gallery/background_images/visa_banner/', help_text=_("Upload a background image for the visa banner."))
    title = models.CharField(max_length=50, blank=True, null=True, help_text=_("Enter an optional title for the visa banner."))
    is_active = models.BooleanField(default=False, help_text=_("Activate this banner."))

    def __str__(self):
        return self.title or f"Background Image {self.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self._compress_image(self.image, (1920, 1080))  # Adjust size as needed

    def _compress_image(self, image_field, size):
        original_path = image_field.path
        image = PILImage.open(image_field)  # Use PILImage to avoid conflict with your Image model
        image = image.resize(size, PILImage.Resampling.LANCZOS)
        im_io = BytesIO()
        image.save(im_io, format='JPEG', quality=85)
        new_image = ContentFile(im_io.getvalue(), name=os.path.basename(original_path))

        if os.path.exists(original_path):
            os.remove(original_path)

        image_field.save(os.path.basename(original_path), new_image, save=False)

class VisaType(models.Model):
    """
    Model to represent types of visas for different countries.
    """
    name = models.CharField(max_length=200)
    description = RichTextField(null=True, blank=True, verbose_name=_('Description'))
    country = models.ForeignKey(Country, related_name='visa_types', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.country}"

class VisaPackage(models.Model):
    """
    Model to represent visa packages including details like overview, description, requirements, etc.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    country = models.ForeignKey(Country, related_name='visa_packages', on_delete=models.CASCADE)
    visa_type = models.ForeignKey(VisaType, related_name='visa_packages', on_delete=models.CASCADE)
    overview = RichTextField()
    requirements = models.ManyToManyField('self', symmetrical=False, through='RequiredDocuments', related_name='related_documents', blank=True)
    
    valid_for = models.CharField(blank=True,null=True, max_length=100, help_text="Validity period of the visa, e.g., 90 days after issued")
    number_of_entries = models.CharField(blank=True,null=True, max_length=50, help_text="Number of entries allowed, e.g., single entry")
    max_stay = models.CharField(blank=True,null=True, max_length=50, help_text="Maximum stay per entry, e.g., 30 days per entry")

    visa_fee = models.DecimalField(max_digits=10, decimal_places=2)
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # Total fee will be calculated automatically
    our_processing_time = models.CharField(blank=True,null=True, max_length=100, help_text="Processing time, e.g., 1 days, 5 hours, 1-2 days/hours ")
    visa_processing_time = models.CharField(blank=True,null=True, max_length=100, help_text="Processing time, e.g., 1 days, 5 hours, 1-2 days/hours ")
    image = models.ImageField(upload_to='gallery/visa_images/images/')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Visa Package"
        verbose_name_plural = "Visa Packages"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Calculate total fee
        self.total_fee = self.visa_fee + self.processing_fee
        # Ensure slug is generated if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        if self.image:
            self._compress_image(self.image, (800, 600))  # Adjust size as needed

    def _compress_image(self, image_field, size):
        original_path = image_field.path
        image = PILImage.open(image_field)  # Use PILImage to avoid conflict with your Image model
        image = image.resize(size, PILImage.Resampling.LANCZOS)
        im_io = BytesIO()
        image.save(im_io, format='JPEG', quality=85)
        new_image = ContentFile(im_io.getvalue(), name=os.path.basename(original_path))

        if os.path.exists(original_path):
            os.remove(original_path)

        image_field.save(os.path.basename(original_path), new_image, save=False)

class RequiredDocuments(models.Model):
    visa_package = models.ForeignKey(VisaPackage, related_name='required_documents', on_delete=models.CASCADE)
    document_for = models.CharField(max_length=200, verbose_name=_('Document For'), help_text=_('Specify who this document is required for (e.g., traveler type)'))
    description = RichTextField(verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Required Document')
        verbose_name_plural = _('Required Documents')

    def __str__(self):
        return f"{self.visa_package.title} - {self.document_for}"
