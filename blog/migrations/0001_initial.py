# Generated by Django 4.2.14 on 2024-08-14 15:45

import blog.models
import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackgroundImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='background_images/')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, validators=[blog.models.validate_unique_category_name], verbose_name='Category Name')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('body', models.TextField(verbose_name='Body')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('approved', models.BooleanField(default=False, verbose_name='Approved')),
            ],
            options={
                'verbose_name': 'Comment',
                'ordering': ['created_on'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('content', ckeditor.fields.RichTextField(verbose_name='Content')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='Updated On')),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='blog/images/', verbose_name='Featured Image')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True, verbose_name='Slug')),
                ('status', models.IntegerField(choices=[(0, 'Draft'), (1, 'Published')], default=0, verbose_name='Status')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Is Featured')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
            ],
            options={
                'verbose_name': 'Blog Post',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('posts', models.ManyToManyField(related_name='tags', to='blog.post', verbose_name='Posts')),
            ],
            options={
                'verbose_name': 'Tag',
            },
        ),
    ]
