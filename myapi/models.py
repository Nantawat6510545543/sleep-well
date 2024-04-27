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
    sleep_duration = models.FloatField()
    sleep_comment = models.CharField(max_length=255, default="No comments")
    sleep_score = models.IntegerField()


class Weather(models.Model):
    weather_id = models.AutoField(primary_key=True)
    lat = models.FloatField()
    lon = models.FloatField()
    timestamp = models.DateTimeField()
    temp_c = models.FloatField()
    condition_text = models.CharField(max_length=100)
    precip_mm = models.FloatField()
    humidity = models.IntegerField()
    location_name = models.CharField(max_length=100, default="Nonthaburi")
    region = models.CharField(max_length=100, default="Nonthaburi")
    country = models.CharField(max_length=100, default="Thailand")
    tz_id = models.CharField(max_length=50, default="Asia/Bangkok")


class Noise(models.Model):
    noise_id = models.AutoField(primary_key=True)
    lat = models.FloatField(default=13.857139052152801)
    lon = models.FloatField(default=100.48867194387923)
    timestamp = models.DateTimeField()
    noise = models.FloatField()
    location_name = models.CharField(max_length=100, default="Nonthaburi")
    region = models.CharField(max_length=100, default="Nonthaburi")
    country = models.CharField(max_length=100, default="Thailand")
    tz_id = models.CharField(max_length=50, default="Asia/Bangkok")
