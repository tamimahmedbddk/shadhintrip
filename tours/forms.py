from django import forms
from .models import TourItinerary

class TourItineraryForm(forms.ModelForm):
    class Meta:
        model = TourItinerary
        exclude = ('tour', 'group_event')
