from django import forms 
from .models import Driver, Accident
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class DriverForm(forms.ModelForm): 
    class Meta: 
        model = Driver 
        fields = ['profile_pic', 'driver_id', 'license_no', 'vehicle_number', 'vehicle_type', 'balance']


class AccidentForm(forms.ModelForm):
    class Meta:
        model= Accident 
        fields = ['location','highlight','detail']


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.TextInput(attrs={'type': 'password'})
    )
    email = forms.CharField(
        label="Email",
        widget=forms.TextInput(attrs={'type': 'email'})
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email','first_name','last_name')  # Include email if needed