# Generated by Django 4.2.6 on 2024-06-04 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visa', '0003_visapackage_refund_policy_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visapackage',
            name='our_processing_time',
            field=models.CharField(blank=True, help_text='Processing time, e.g., 1 days, 5 hous, 1-2 days/hours ', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='visapackage',
            name='visa_processing_time',
            field=models.CharField(blank=True, help_text='Processing time, e.g., 1 days, 5 hous, 1-2 days/hours ', max_length=100, null=True),
        ),
    ]