from django.db import models


class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    sex = models.CharField(max_length=10)
    age = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()


class Sleep(models.Model):
    sleep_id = models.AutoField(primary_key=True)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    sleep_time = models.DateTimeField()
    lat = models.FloatField()
    lon = models.FloatField()
    sleep_duration = models.IntegerField()
    sleep_comments = models.CharField(max_length=255, default="No comments")
    sleep_score = models.IntegerField()


class Weather(models.Model):
    weather_api_id = models.AutoField(primary_key=True)
    lat = models.FloatField()
    lon = models.FloatField()
    timestamp = models.DateTimeField()
    temp_c = models.FloatField()
    condition_text = models.CharField(max_length=100)
    precip_mm = models.FloatField()
    humidity = models.IntegerField()


class NoiseStation(models.Model):
    station_id = models.AutoField(primary_key=True)
    lat = models.FloatField()
    lon = models.FloatField()
    timestamp = models.DateTimeField()
    noise = models.FloatField()
    location_name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    tz_id = models.CharField(max_length=50)
