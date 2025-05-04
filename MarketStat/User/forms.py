from django import forms
from .models import *

class CollectionForm(forms.Form):
    collectionId = forms.IntegerField(required=True)
    quantity = forms.IntegerField(min_value=1, required=True)
    initialPrice = forms.DecimalField(min_value=1, required=True, decimal_places=4)

class SellForm(forms.Form):
    soldTo = forms.CharField(required=False)
    soldQuantity = forms.IntegerField(min_value=1, required=True)
    soldPrice = forms.DecimalField(min_value=1, required=True, decimal_places=4)

class updateForm(forms.Form):
    changedQuantity = forms.IntegerField(min_value=1, required=False)
    changedPrice = forms.DecimalField(min_value=1, required=False)