# Generated by Django 4.2.6 on 2024-06-04 18:02

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visa', '0004_alter_visapackage_our_processing_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='visapackage',
            name='general_documents_required',
            field=ckeditor.fields.RichTextField(blank=True, help_text='Documents required for all applicants', null=True, verbose_name='General Documents Required'),
        ),
    ]
