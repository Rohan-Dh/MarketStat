from django import forms
from .models import *

class CollectionForm(forms.Form):
    collectionId = forms.IntegerField(required=True)
    quantity = forms.IntegerField(min_value=1, required=True)
    initialPrice = forms.DecimalField(required=True, decimal_places=4)