from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import generics


from myapi.analytics import analyze_opinions
from myapi.models import Sleep, Person, Weather, Noise
from myapi.serializers import SleepInfoSerializer, PersonInfoSerializer, \
    SleepInfoAnalyticsSerializer
from myapi.utils import get_closest_station, get_environments, get_sleep_within_range


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
    """
    serializer_class = SleepInfoSerializer

    def get_queryset(self):
        sleeps = Sleep.objects.all()

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


class SleepInfoAnalyticsView(generics.ListAPIView):
    """
    Returns analytics data for sleep information, including average sleep scores, opinion analytics based on sleep comments, and environmental data for each person.
    """
    serializer_class = SleepInfoAnalyticsSerializer

    def get_queryset(self):
        persons = Person.objects.all()

        data = []
        for person in persons:
            sleeps = (Sleep.objects.filter(person_id=person.person_id)
                      .select_related('person'))
            average_score = sleeps.aggregate(avg_score=Avg('sleep_score'))[
                'avg_score']
            sleep_comments = [sleep.sleep_comment for sleep in sleeps]
            opinion_analytics = analyze_opinions(sleep_comments)
            environment = get_environments(sleeps)

            data.append({
                'person_info': person,
                'average_score': average_score,
                'opinion_analytics': opinion_analytics,
                'environment': environment,
            })

        return data


class SleepInfoAnalyticsViewByPerson(generics.RetrieveAPIView):
    """Returns analytics data for sleep information related to a specific person identified by person_id, including average sleep scores, opinion analytics based on sleep comments, and environmental data."""
    serializer_class = SleepInfoAnalyticsSerializer

    def get_object(self):
        person_id = self.kwargs.get('person_id')
        person_info = Person.objects.filter(person_id=person_id).first()

        sleeps = Sleep.objects.filter(person_id=person_id).select_related(
            'person')
        average_score = sleeps.aggregate(avg_score=Avg('sleep_score'))[
            'avg_score']
        sleep_comments = [sleep.sleep_comment for sleep in sleeps]
        opinion_analytics = analyze_opinions(sleep_comments)

        environment = get_environments(sleeps)

        return {
            'person_info': person_info,
            'average_score': average_score,
            'opinion_analytics': opinion_analytics,
            'environment': environment,
        }
