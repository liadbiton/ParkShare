# Generated by Django 5.1.3 on 2024-11-30 23:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apartment_number', models.CharField(max_length=10, unique=True)),
                ('building_name', models.CharField(max_length=50)),
                ('helping_score', models.IntegerField(default=0)),
                ('using_score', models.IntegerField(default=0)),
                ('cars', models.ManyToManyField(blank=True, related_name='apartments', to='parking.car')),
            ],
        ),
        migrations.CreateModel(
            name='ParkingSpot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spot_number', models.CharField(max_length=10)),
                ('floor', models.CharField(choices=[('0', 'Ground Floor'), ('-1', 'Basement 1'), ('-2', 'Basement 2')], max_length=2)),
                ('is_free', models.BooleanField(default=True)),
                ('free_from', models.DateTimeField(blank=True, null=True)),
                ('free_until', models.DateTimeField(blank=True, null=True)),
                ('reserved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reserved_spots', to='parking.apartment')),
                ('reserved_for_car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reserved_parking_spot', to='parking.car')),
            ],
            options={
                'unique_together': {('spot_number', 'floor')},
            },
        ),
    ]
