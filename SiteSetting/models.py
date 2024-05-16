from django.db import models
from ckeditor.fields import RichTextField
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', help_text="Main logo for the site", blank=True, null=True)
    favicon = models.ImageField(upload_to='favicons/', help_text="Favicon for the site", blank=True, null=True)
    about_content = RichTextField(help_text="Content for the about page", blank=True, null=True)
    privacy_policy_content = RichTextField(help_text="Content for the privacy policy page", blank=True, null=True)
    terms_of_service = RichTextField(help_text="Content for the terms page", blank=True, null=True)
    cancellation_policy = RichTextField(help_text="Content for the cancellation policy page", blank=True, null=True)
    refund_policy = RichTextField(help_text="Content for the refund_policy page", blank=True, null=True)
    faq = RichTextField(help_text="Content for the faq page", blank=True, null=True)


    def __str__(self):
        return self.site_name

class BackgroundImage(models.Model):
    image = models.ImageField(upload_to='background_images/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Background Image {self.id}"
    
class BackgroundVideo(models.Model):
    video = models.FileField(upload_to='background_videos/')
    is_active = models.BooleanField(default=True)

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

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon_class = models.CharField(max_length=100, help_text="Class name for the icon")

    def __str__(self):
        return f"{self.get_platform_display()}"

class ContactInfo(models.Model):
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return "Contact Information"
