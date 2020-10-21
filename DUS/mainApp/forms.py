from django import forms
from .models import ContactUsModel
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class ConatcUsForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    class Meta:
        model = ContactUsModel
        fields = '__all__'

        

    def save(self, commit=True):
        contactus = super().save(commit=False)
        if commit:
            contactus.save()
        return contactus
