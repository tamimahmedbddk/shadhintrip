from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator  # Import MinValueValidator
from django.utils.translation import gettext_lazy as _
from SiteSetting.models import Country

User = get_user_model()

class VisaBanner(models.Model):
    image = models.ImageField(upload_to='gallery/visa_images/visa_banner/')
    title = models.CharField(max_length=50, blank=True,null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Background Image {self.id}"

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
    our_processing_time = models.CharField(blank=True,null=True, max_length=100, help_text="Processing time, e.g., 1 days, 5 hous, 1-2 days/hours ")
    visa_processing_time = models.CharField(blank=True,null=True, max_length=100, help_text="Processing time, e.g., 1 days, 5 hous, 1-2 days/hours ")
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

class RequiredDocuments(models.Model):
    visa_package = models.ForeignKey(VisaPackage, related_name='required_documents', on_delete=models.CASCADE)
    document_for = models.CharField(max_length=200, verbose_name=_('Document For'), help_text=_('Specify who this document is required for (e.g., traveler type)'))
    description = RichTextField(verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Required Document')
        verbose_name_plural = _('Required Documents')

    def __str__(self):
        return f"{self.visa_package.title} - {self.document_for}"

