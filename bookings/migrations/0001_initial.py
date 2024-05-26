# Generated by Django 4.2.6 on 2024-05-26 04:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TourBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('confirmation_date', models.DateTimeField(blank=True, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('paid_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('payment_method', models.CharField(choices=[('online', 'Online Payment'), ('cash', 'Cash on Delivery'), ('bank_transfer', 'Bank Transfer')], default='online', max_length=20)),
                ('payment_reference', models.CharField(blank=True, max_length=100)),
                ('payment_received_by', models.CharField(blank=True, max_length=100)),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Tour Bookings',
            },
        ),
        migrations.CreateModel(
            name='VisaBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('confirmation_date', models.DateTimeField(blank=True, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('paid_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('payment_method', models.CharField(choices=[('online', 'Online Payment'), ('cash', 'Cash on Delivery'), ('bank_transfer', 'Bank Transfer')], default='online', max_length=20)),
                ('payment_reference', models.CharField(blank=True, max_length=100)),
                ('payment_received_by', models.CharField(blank=True, max_length=100)),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Visa Bookings',
            },
        ),
    ]
