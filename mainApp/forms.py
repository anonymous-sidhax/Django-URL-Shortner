from django import forms
from .models import ContactUs
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class ContactUsForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    terms_and_conditions = forms.BooleanField()
    class Meta:
        model = ContactUs
        fields = '__all__'

        

    def save(self, commit=True):
        contactus = super().save(commit=False)
        if commit:
            contactus.save()
        return contactus
