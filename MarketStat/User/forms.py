from django import forms
from .validators import validateImage
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.conf import settings
import random
from .models import *

from django.contrib.auth import get_user_model
User = get_user_model()

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

class UserProfileForm(forms.Form):
    firstName = forms.CharField(max_length=100, required=True)
    lastName = forms.CharField(max_length=100, required=False)
    address = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        code = "{:04d}".format(random.randint(0, 9999))
        subject = "Verify your email"
        plain_message = f"Your verification code is: {code}"
        html_message = f"""
            <div style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
                <h2 style="color: #2c3e50;">Market Stat</h2>
                <p>Hello,</p>
                <p>Your verification code is:</p>
                <h1 style="color: #27ae60;">{code}</h1>
                <p>Please use this code to verify your email address.</p>
                <br/>
                <small>Thank you!</small>
            </div>
        """
        userObj = get_object_or_404(User, id = self.request.user.id)
        if not userObj.email == email:
            try:
                send_mail(
                    subject, 
                    plain_message, 
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                    html_message=html_message,
                    )
            except Exception:
                raise ValidationError("Unexpected error occurred while sending the email.")
        
        if self.request:
            self.request.session['email_verification_code'] = code

        return email
        
        

class ProfilePictureForm(forms.Form):
    profilePic = forms.ImageField(validators=[validateImage])
