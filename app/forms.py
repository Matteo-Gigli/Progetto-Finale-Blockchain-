from django import forms
from .models import Item

'''We built a forms to make an offer for the Item
Come back to app/views.py '''

class MakeAnOffer(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['offer']
