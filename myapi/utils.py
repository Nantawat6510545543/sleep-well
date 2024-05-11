import numpy as np

from datetime import timedelta
from geopy.distance import geodesic
from textblob import TextBlob

from myapi.models import *
from django.db.models import Avg


def get_closest_station(sleep: Sleep, stations: models.Model):
    closest = None
    closest_dist = float('inf')
    max_time_difference = timedelta(hours=12)

    for station in stations.objects.all():
        distance = geodesic((sleep.lat, sleep.lon), (station.lat, station.lon)).km

        time_difference = abs(station.timestamp - sleep.sleep_time)
        within_time_limit = time_difference <= max_time_difference

        if distance <= 5 and within_time_limit:
            if distance < closest_dist:
                closest = station
                closest_dist = distance

    return closest


def get_sleep_within_range(lat, lon, range_km):
    sleeps_within_range = []

    for sleep in Sleep.objects.all():
        distance_km = geodesic((sleep.lat, sleep.lon), (lat, lon)).km

        if distance_km <= range_km:
            sleeps_within_range.append(sleep)

    return sleeps_within_range


def get_average(data: list[models.Model], attribute: str):
    valid_data = [getattr(station, attribute) for station in data if station is not None]
    return np.mean(valid_data) if valid_data else None


def get_environments(sleeps):
    closest_weather_list = [get_closest_station(sleep, Weather) for sleep in
                            sleeps]
    closest_noise_station_list = [get_closest_station(sleep, Noise) for sleep in
                                  sleeps]

    avg_temp_c = get_average(closest_weather_list, "temp_c")
    avg_precip_mm = get_average(closest_weather_list, "precip_mm")
    avg_humidity = get_average(closest_weather_list, "humidity")
    avg_noise = get_average(closest_noise_station_list, "noise")

    context = {
        'avg_temp_c': avg_temp_c,
        'avg_precip_mm': avg_precip_mm,
        'avg_humidity': avg_humidity,
        'avg_noise': avg_noise,
    }

    return context


def get_sentiment(comment):
    """
    >>> get_sentiments("I love this product!")
    0.5
    >>> get_sentiments("This movie is terrible.")
    -1.0
    >>> get_sentiments("The weather is nice today.")
    0.6
    """
    return TextBlob(comment).sentiment.polarity


def get_analytics_data(person_id):
    sleeps = Sleep.objects.filter(person_id=person_id).select_related('person')
    average_score = sleeps.aggregate(avg_score=Avg('sleep_score'))['avg_score']
    comments_list = sleeps.values_list('sleep_comment', flat=True)

    sentiments_list = [get_sentiment(comment) for comment in comments_list]
    average_sentiment = np.mean(sentiments_list) if sentiments_list else None

    return {
        'person_id': person_id,
        'average_score': average_score,
        'opinion_analytics': {
            'average_sentiment': average_sentiment,
            'total_comments': comments_list.count()
        },
        'environment': get_environments(sleeps),
    }
