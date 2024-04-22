from datetime import timedelta
from math import radians, sin, cos, sqrt, atan2
from typing import List

from . import models


def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Radius of the Earth in kilometers
    return distance


def get_closest(sleep: models.Sleep, stations: models):
    closest = None
    closest_dist = float('inf')
    max_time_difference = timedelta(hours=12)

    for station in stations.objects.all():
        distance = haversine(sleep.lat, sleep.lon, station.lat, station.lon)

        time_difference = abs(station.timestamp - sleep.sleep_time)
        within_time_limit = time_difference <= max_time_difference

        if distance <= 5 and within_time_limit:
            if distance < closest_dist:
                closest = station
                closest_dist = distance

    return closest


def get_average(data: List, attribute: str):
    valid_data = [getattr(station, attribute) for station in data if
                  station is not None]
    return sum(valid_data) / len(valid_data) if valid_data else None


def get_environments(sleeps):
    closest_weather_list = [get_closest(sleep, models.Weather) for sleep in
                            sleeps]
    closest_noise_station_list = [get_closest(sleep, models.Noise) for sleep in
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
