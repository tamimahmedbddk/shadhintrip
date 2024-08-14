# Generated by Django 4.2.14 on 2024-08-14 10:06

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackgroundImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Upload a background image.', upload_to='background_images/')),
                ('is_active', models.BooleanField(default=True, help_text='Activate this background image.')),
            ],
        ),
        migrations.CreateModel(
            name='BackgroundVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(help_text='Upload a background video.', upload_to='background_videos/')),
                ('is_active', models.BooleanField(default=True, help_text='Activate this background video.')),
            ],
        ),
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(help_text='Enter the contact phone number.', max_length=20)),
                ('email', models.EmailField(help_text='Enter the contact email address.', max_length=254)),
                ('address', models.TextField(help_text='Enter the contact address.')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the name of the country.', max_length=200, unique=True)),
                ('image', models.ImageField(help_text='Upload an image representing the country.', upload_to='country_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Favicon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Upload the favicon for the site.', upload_to='favicons/')),
                ('is_active', models.BooleanField(default=True, help_text='Activate this favicon.')),
            ],
        ),
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Upload the main logo for the site.', upload_to='logos/')),
                ('is_active', models.BooleanField(default=True, help_text='Activate this logo.')),
            ],
        ),
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_image', models.ImageField(blank=True, help_text='Upload the banner image for the site.', null=True, upload_to='background_images/')),
                ('about_content', ckeditor.fields.RichTextField(blank=True, help_text='Content for the about page.', null=True)),
                ('privacy_policy_content', ckeditor.fields.RichTextField(blank=True, help_text='Content for the privacy policy page.', null=True)),
                ('terms_of_service', ckeditor.fields.RichTextField(blank=True, help_text='Content for the terms of service page.', null=True)),
                ('cancellation_policy', ckeditor.fields.RichTextField(blank=True, help_text='Content for the cancellation policy page.', null=True)),
                ('refund_policy', ckeditor.fields.RichTextField(blank=True, help_text='Content for the refund policy page.', null=True)),
                ('faq', ckeditor.fields.RichTextField(blank=True, help_text='Content for the FAQ page.', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('instagram', 'Instagram'), ('linkedin', 'LinkedIn'), ('youtube', 'YouTube')], help_text='Select the social media platform.', max_length=20)),
                ('url', models.URLField(help_text='Enter the URL for the social media profile.')),
                ('icon_class', models.CharField(blank=True, help_text='Class name for the icon.', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the name of the city.', max_length=200)),
                ('country', models.ForeignKey(help_text='Select the country this city belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='SiteSetting.country')),
            ],
        ),
    ]
