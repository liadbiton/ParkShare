from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, CarForm, ParkingSpotForm
from .models import ParkingSpot
from .models import Apartment
from .forms import AssignApartmentForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save()
            request.user.apartment.cars.add(car)
            return redirect('home')
    else:
        form = CarForm()
    return render(request, 'parking/add_car.html', {'form': form})


@login_required
def mark_parking_spot_free(request):
    if request.method == 'POST':
        form = ParkingSpotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ParkingSpotForm()
    return render(request, 'parking/mark_parking_free.html', {'form': form})


def home(request):
    if request.user.is_authenticated:
        # If user is logged in, redirect to the dashboard
        return redirect('dashboard')
    else:
        return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Create an Apartment for the newly created user
            Apartment.objects.create(user=user)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    if not hasattr(request.user, 'apartment'):
        return redirect('assign_apartment')  # Redirect to assign apartment page if the user has no apartment

    apartment = request.user.apartment
    return render(request, 'parking/dashboard.html', {'apartment': apartment})


@login_required
def assign_apartment(request):
    try:
        apartment = request.user.apartment
        form = AssignApartmentForm(instance=apartment)
    except Apartment.DoesNotExist:
        apartment = None
        form = AssignApartmentForm()

    if request.method == 'POST':
        form = AssignApartmentForm(request.POST, instance=apartment)
        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.user = request.user
            apartment.save()
            return redirect('dashboard')  # Redirect to a suitable page after saving

    return render(request, 'parking/assign_apartment.html', {'form': form})