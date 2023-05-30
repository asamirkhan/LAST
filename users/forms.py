from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={"class": "form-control"})
        )

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
        

class CustomAuthenticationForm(AuthenticationForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
                "class": "form-control", 
                "id": "floatingPassword"
            })
        )
    username = forms.CharField(
        label='Пароль',
        widget=forms.TextInput(attrs={
                "class": "form-control", 
                "id": "floatingInput"
            })
        )


class AuthorEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'about_me', 'avatar')
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "about_me": forms.Textarea(attrs={"class": "form-control"}),
        }
        
