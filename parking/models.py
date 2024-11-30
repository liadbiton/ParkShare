from django.db import models
from datetime import datetime
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone


class Car(models.Model):
    car_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.car_number

    def save(self, *args, **kwargs):
        # Custom save method to validate that no duplicate car numbers are saved.
        if Car.objects.filter(car_number=self.car_number).exists():
            raise ValueError(f"A car with number {self.car_number} already exists.")
        super(Car, self).save(*args, **kwargs)


class Apartment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='apartment', null=True, blank=True)
    apartment_number = models.CharField(max_length=10, unique=True)
    building_name = models.CharField(max_length=50)
    cars = models.ManyToManyField(Car, related_name='apartments', blank=True)
    helping_score = models.IntegerField(default=0)
    using_score = models.IntegerField(default=0)

    def __str__(self):
        return f"Apartment {self.apartment_number} in {self.building_name}"

    @property
    def balance(self):
        return self.helping_score - self.using_score

    def add_car(self, car_number):
        car, created = Car.objects.get_or_create(car_number=car_number)
        self.cars.add(car)
        self.save()


class ParkingSpot(models.Model):
    FLOOR_CHOICES = [
        ('0', 'Ground Floor'),
        ('-1', 'Basement 1'),
        ('-2', 'Basement 2'),
    ]

    spot_number = models.CharField(max_length=10)
    floor = models.CharField(max_length=2, choices=FLOOR_CHOICES)
    is_free = models.BooleanField(default=True)
    reserved_by = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='reserved_spots')
    reserved_for_car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='reserved_parking_spot')
    free_from = models.DateTimeField(null=True, blank=True)
    free_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('spot_number', 'floor')

    def __str__(self):
        return f"Spot {self.spot_number} on Floor {self.floor}"

    def mark_as_free(self, free_from, free_until):
        self.is_free = True
        self.free_from = free_from
        self.free_until = free_until
        self.reserved_by = None
        self.reserved_for_car = None
        self.save()

    def reserve(self, apartment, car, from_time, until_time):
        if not self.is_free:
            raise ValueError(f"Parking spot {self} is already reserved.")
        self.is_free = False
        self.reserved_by = apartment
        self.reserved_for_car = car
        self.free_from = from_time
        self.free_until = until_time
        self.save()

    def cancel_reservation(self):
        self.is_free = True
        self.reserved_by = None
        self.reserved_for_car = None
        self.free_from = None
        self.free_until = None
        self.save()

    def find_available_spots(cls, from_time: datetime, until_time: datetime):
        """
        Class method to find all available parking spots within a given time range.
        """
        return cls.objects.filter(
            is_free=True,
            free_from__lte=from_time,
            free_until__gte=until_time
        )

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
            apartment = Apartment.objects.create(
                apartment_number=self.cleaned_data['apartment_number'],
                building_name=self.cleaned_data['building_name']
            )
        return user

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_number']

class ParkingSpotForm(forms.ModelForm):
    class Meta:
        model = ParkingSpot
        fields = ['spot_number', 'floor', 'free_from', 'free_until']

# Migration command:
# After creating this model, run the following commands to create the database schema:
# python manage.py makemigrations
# python manage.py migrate
