from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from PIL import Image
from django.core.exceptions import ValidationError

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
    image = models.ImageField(upload_to='gallery/blog_images/blog_banner/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Background Image {self.id}"
    
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
    featured_image = models.ImageField(upload_to='gallery/blog_images/images/', null=True, blank=True, verbose_name="Featured Image")
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
        Override save method to generate slug and resize featured image.
        """
        if not self.slug:
            self.slug = custom_slugify(self.title)

        super().save(*args, **kwargs)

        if self.featured_image:
            image = Image.open(self.featured_image)
            image = image.resize((600, 450), Image.Resampling.LANCZOS)
            image.save(self.featured_image.path)

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
