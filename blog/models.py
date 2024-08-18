from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from PIL import Image
from django.core.exceptions import ValidationError

from io import BytesIO
from django.core.files.base import ContentFile
import os

User = get_user_model()

def custom_slugify(value, allow_unicode=False):
    """
    Create a slug for the given value.
    """
    if allow_unicode:
        value = slugify(value)
    else:
        value = slugify(value)
    return value

def validate_unique_category_name(value):
    """
    Validate that the category name is unique.
    """
    if Category.objects.filter(name=value).exists():
        raise ValidationError('A category with this name already exists.')

class BackgroundImage(models.Model):
    """
    Model to store background images.
    """
    image = models.ImageField(upload_to='background_images/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Background Image {self.id}"

    def save(self, *args, **kwargs):
        # First, save the model to ensure the image field has a path
        if not self.pk:
            super().save(*args, **kwargs)

        if self.image:
            # Get the original file path
            original_path = self.image.path

            # Open the image file
            image = Image.open(self.image)

            # Resize and compress the image
            image = image.resize((1920, 1080), Image.Resampling.LANCZOS)
            im_io = BytesIO()
            image.save(im_io, format='JPEG', quality=85)
            new_image = ContentFile(im_io.getvalue(), name=os.path.basename(original_path))

            # Delete the old file to prevent duplication
            if os.path.exists(original_path):
                os.remove(original_path)

            # Overwrite the existing image file with the new one
            self.image.save(os.path.basename(original_path), new_image, save=False)

        # Now save the model instance without triggering another image save
        super().save(update_fields=['is_active'])
    
class Category(models.Model):
    """
    Model to represent categories.
    """
    name = models.CharField(max_length=200, validators=[validate_unique_category_name], verbose_name="Category Name")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    Model to represent blog posts.
    """
    title = models.CharField(max_length=200, verbose_name="Title")
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, verbose_name="Author")
    content = RichTextField(verbose_name="Content")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Updated On")
    featured_image = models.ImageField(upload_to='blog/images/', null=True, blank=True, verbose_name="Featured Image")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="Slug")
    status = models.IntegerField(choices=((0,"Draft"), (1,"Published")), default=0, verbose_name="Status")
    category = models.ForeignKey(Category, related_name='blog_posts', on_delete=models.CASCADE, verbose_name="Category")
    is_featured = models.BooleanField(default=False, verbose_name="Is Featured")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    class Meta:
        ordering = ['-created_on']
        verbose_name = "Blog Post"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Override save method to generate slug, resize, and compress featured image.
        """
        if not self.slug:
            self.slug = custom_slugify(self.title)

        # Save the model first to ensure the image file has a path
        super().save(*args, **kwargs)

        if self.featured_image:
            # Get the original file path
            original_path = self.featured_image.path

            # Open the image file
            image = Image.open(self.featured_image)

            # Resize and compress the image
            image = image.resize((1920, 1080), Image.Resampling.LANCZOS)
            im_io = BytesIO()
            image.save(im_io, format='JPEG', quality=85)
            new_image = ContentFile(im_io.getvalue(), name=os.path.basename(original_path))

            # Delete the old file to prevent duplication
            if os.path.exists(original_path):
                os.remove(original_path)

            # Overwrite the existing image file with the new one
            self.featured_image.save(os.path.basename(original_path), new_image, save=False)

        # Finally, save the model instance without triggering another image save
        super().save(update_fields=['title', 'slug', 'content', 'category', 'status', 'is_featured', 'is_active'])

class Comment(models.Model):
    """
    Model to represent comments on blog posts.
    """
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, verbose_name="Post")
    name = models.CharField(max_length=80, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    body = models.TextField(verbose_name="Body")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Created On")
    approved = models.BooleanField(default=False, verbose_name="Approved")

    class Meta:
        ordering = ['created_on']
        verbose_name = "Comment"

    def __str__(self):
        return f"Comment {self.body} by {self.name}"

class Tag(models.Model):
    """
    Model to represent tags for blog posts.
    """
    name = models.CharField(max_length=100, verbose_name="Name")
    posts = models.ManyToManyField(Post, related_name='tags', verbose_name="Posts")

    class Meta:
        verbose_name = "Tag"

    def __str__(self):
        return self.name
