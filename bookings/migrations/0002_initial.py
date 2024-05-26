# Generated by Django 4.2.6 on 2024-05-26 04:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookings', '0001_initial'),
        ('tours', '0001_initial'),
        ('visa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visabooking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visa_bookings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='visabooking',
            name='visa_package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='visa.visapackage'),
        ),
        migrations.AddField(
            model_name='tourbooking',
            name='group_event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tours.groupevent'),
        ),
        migrations.AddField(
            model_name='tourbooking',
            name='tour',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tours.tour'),
        ),
        migrations.AddField(
            model_name='tourbooking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour_bookings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='tourbooking',
            constraint=models.UniqueConstraint(fields=('user', 'tour'), name='unique_tour_booking'),
        ),
        migrations.AddConstraint(
            model_name='tourbooking',
            constraint=models.UniqueConstraint(fields=('user', 'group_event'), name='unique_group_event_booking'),
        ),
    ]
