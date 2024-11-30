from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Car, ParkingSpot
from .models import Apartment

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    apartment_number = forms.CharField(max_length=10)
    building_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'apartment_number', 'building_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_number']


class ParkingSpotForm(forms.ModelForm):
    class Meta:
        model = ParkingSpot
        fields = ['spot_number', 'floor', 'free_from', 'free_until']


class AssignApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['apartment_number', 'building_name', 'helping_score', 'using_score']
        labels = {
            'apartment_number': 'Apartment Number',
            'building_name': 'Building Name',
            'helping_score': 'Helping Score',
            'using_score': 'Using Score',
        }