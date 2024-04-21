from datetime import timedelta
from math import radians, sin, cos, sqrt, atan2


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


# def get_closest(sleep, models):
#     closest = None
#     closest_dist = float('inf')
#
#     models_within_5km = models.objects.filter(
#         lat__lte=sleep.lat + 0.05,
#         lat__gte=sleep.lat - 0.05,
#         lon__lte=sleep.lon + 0.05,
#         lon__gte=sleep.lon - 0.05,
#         timestamp__gte=sleep.sleep_time - timedelta(hours=24),
#         timestamp__lte=sleep.sleep_time + timedelta(hours=24),
#     )
#
#     for model in models_within_5km:
#         dist = haversine(sleep.lat, sleep.lon, model.lat, model.lon)
#         if dist < closest_dist:
#             closest = model
#             closest_dist = dist
#
#     return closest

def get_closest(sleep, stations):
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
