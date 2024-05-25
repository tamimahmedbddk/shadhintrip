# Generated by Django 4.2.6 on 2024-05-25 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SiteSetting', '0003_remove_logo_site_sitesettings_favicon_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favicon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Upload the favicon for the site.', upload_to='favicons/')),
            ],
        ),
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='Upload the main logo for the site.', upload_to='logos/')),
            ],
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='favicon',
        ),
        migrations.RemoveField(
            model_name='sitesettings',
            name='logo',
        ),
    ]