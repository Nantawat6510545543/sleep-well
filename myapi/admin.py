from django.contrib import admin
from .models import Person, Sleep, Weather, Noise


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('person_id', 'sex', 'age', 'height', 'weight')


@admin.register(Sleep)
class SleepAdmin(admin.ModelAdmin):
    list_display = (
        'sleep_id', 'person', 'sleep_time', 'sleep_duration', 'sleep_score')


@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = (
        'weather_id', 'lat', 'lon', 'timestamp', 'temp_c', 'condition_text',
        'precip_mm', 'humidity', 'location_name', 'region', 'country', 'tz_id')


@admin.register(Noise)
class NoiseAdmin(admin.ModelAdmin):
    list_display = (
        'noise_id', 'lat', 'lon', 'timestamp', 'noise', 'location_name',
        'region', 'country', 'tz_id')
