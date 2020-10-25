from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password',)



        # def clean_username(self):
        #     username = self.cleaned_data.get('username')
        #     password = self.cleaned_data.get('password')
            
        #     if not User.objects.filter(username=username).exists():
        #         raise ValidationError('Please enter a correct username and password. Note that both fields may be case-sensitive')
        #     else:
        #         return username, password














class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User 
        fields = ('username', 'email', 'password1', 'password2',)


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            if email  == User.objects.filter(email=email)[0].email:
                raise ValidationError('Email already used')
            else:
                return email
        except IndexError:
            print(email)
            return email

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

   