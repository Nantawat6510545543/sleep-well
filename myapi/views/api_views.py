from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics

from myapi.models import *
from myapi.serializers import SleepInfoSerializer, PersonInfoSerializer, \
    SleepInfoAnalyticsSerializer
from myapi.utils import get_analytics_data, get_closest_station, get_sleep_within_range


class PersonInfoListView(generics.ListAPIView):
    """Returns a list of Person information."""
    queryset = Person.objects.all()
    serializer_class = PersonInfoSerializer


class PersonInfoView(generics.RetrieveAPIView):
    """Returns detailed information about a specific person identified by person_id."""
    queryset = Person.objects.all()
    serializer_class = PersonInfoSerializer
    lookup_field = 'person_id'


class SleepInfoListView(generics.ListAPIView):
    """
    Returns a list of sleep information with additional data about the closest environment for each sleep entry.
    Can accept optional `day`, `month`, or `year` query parameters to retrieve all sleep entries 
    that occurred on a specific date.
    """
    serializer_class = SleepInfoSerializer

    def get_queryset(self):
        sleeps = Sleep.objects.all()
        filters = Q()

        if "day" in self.request.GET:
            day = self.request.GET.get('day')
            filters &= Q(sleep_time__day=day)

        if "month" in self.request.GET:
            month = self.request.GET.get('month')
            filters &= Q(sleep_time__month=month)
        
        if "year" in self.request.GET:
            year = self.request.GET.get('year')
            filters &= Q(sleep_time__year=year)

        sleeps = sleeps.filter(filters)

        for sleep in sleeps:
            sleep.closest_weather = get_closest_station(sleep, Weather)
            sleep.closest_noise_station = get_closest_station(sleep, Noise)

        return sleeps


class SleepInfoByIdView(generics.RetrieveAPIView):
    """
    Returns detailed sleep information for a specific sleep entry identified by sleep_id, including data about the closest environment.
    """
    serializer_class = SleepInfoSerializer

    def get_object(self):
        sleep = get_object_or_404(Sleep, sleep_id=self.kwargs['sleep_id'])
        sleep.closest_weather = get_closest_station(sleep, Weather)
        sleep.closest_noise_station = get_closest_station(sleep, Noise)
        return sleep


class SleepInfoByPersonView(generics.ListAPIView):
    """
    Returns sleep information for all sleep entries associated with a specific person identified by person_id, including data about the closest environment for each sleep entry.
    """
    serializer_class = SleepInfoSerializer

    def get_queryset(self):
        sleeps = Sleep.objects.filter(person_id=self.kwargs['person_id'])
        for sleep in sleeps:
            sleep.closest_weather = get_closest_station(sleep, Weather)
            sleep.closest_noise_station = get_closest_station(sleep, Noise)
        return sleeps


class SleepInfoByLocationView(generics.ListAPIView):
    """
    Returns sleep information for all sleep entries within a certain range (default range is 5 km) of a specified location (lat and lon coordinates), including data about the closest environment for each sleep entry.
    """
    serializer_class = SleepInfoSerializer

    def get_queryset(self):
        range_km = 5
        lat = self.kwargs['lat']
        lon = self.kwargs['lon']
        if 'km' in self.kwargs:
            range_km = self.kwargs['km']
        sleeps = get_sleep_within_range(lat, lon, range_km)
        for sleep in sleeps:
            sleep.closest_weather = get_closest_station(sleep, Weather)
            sleep.closest_noise_station = get_closest_station(sleep, Noise)
        return sleeps


class SleepInfoByDateView(generics.ListAPIView):
    """
    Returns sleep information for all sleep entries that occurred on a specific date,
    including data about the closest environment for each sleep entry.
    """
    serializer_class = SleepInfoSerializer

    def get_queryset(self):
        sleeps = Sleep.objects.all()
        filters = Q()

        if "day" in self.request.GET:
            day = self.request.GET.get('day')
            filters &= Q(sleep_time__day=day)

        if "month" in self.request.GET:
            month = self.request.GET.get('month')
            filters &= Q(sleep_time__month=month)
        
        if "year" in self.request.GET:
            year = self.request.GET.get('year')
            filters &= Q(sleep_time__year=year)

        sleeps = sleeps.filter(filters)

        for sleep in sleeps:
            sleep.closest_weather = get_closest_station(sleep, Weather)
            sleep.closest_noise_station = get_closest_station(sleep, Noise)
        return sleeps


class SleepInfoAnalyticsView(generics.ListAPIView):
    """
    Returns analytics data for sleep information, including average sleep scores,
    opinion analytics based on sleep comments, and environmental data for each person.
    """
    serializer_class = SleepInfoAnalyticsSerializer

    def get_queryset(self):
        persons = Person.objects.all()
        return [get_analytics_data(person.person_id) for person in persons]


class SleepInfoAnalyticsByPersonView(generics.RetrieveAPIView):
    """
    Returns analytics data for sleep information related to a specific person identified by person_id,
    including average sleep scores, opinion analytics based on sleep comments, and environmental data.
    """
    serializer_class = SleepInfoAnalyticsSerializer

    def get_object(self):
        person_id = self.kwargs.get('person_id')
        return get_analytics_data(person_id)