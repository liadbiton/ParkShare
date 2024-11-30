from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('add_car/', views.add_car, name='add_car'),
    path('mark_parking_spot_free/', views.mark_parking_spot_free, name='mark_parking_spot_free'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('assign_apartment/', views.assign_apartment, name='assign_apartment'),
]
