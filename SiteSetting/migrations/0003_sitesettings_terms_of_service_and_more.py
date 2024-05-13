# Generated by Django 4.2.6 on 2024-05-03 12:39

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SiteSetting', '0002_alter_sitesettings_about_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='terms_of_service',
            field=ckeditor.fields.RichTextField(blank=True, help_text='Content for the terms page', null=True),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='privacy_policy_content',
            field=ckeditor.fields.RichTextField(help_text='Content for the privacy policy page'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='site_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
