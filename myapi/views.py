from django.db.models import Avg
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import render, redirect

from .analytics import analyze_opinions
from .models import Sleep, Person, WeatherAPI, Noise
from .serializers import SleepInfoSerializer, PersonInfoSerializer, \
    SleepInfoAnalyticsSerializer, AverageEnvironmentSerializer


def index(request):
    return render(request, 'myapi/index.html')


class SleepInfoListView(generics.ListAPIView):
    queryset = Sleep.objects.all()
    serializer_class = SleepInfoSerializer


class SleepInfoView(generics.RetrieveAPIView):
    queryset = Sleep.objects.all()
    serializer_class = SleepInfoSerializer
    lookup_field = 'person_id'


class SleepInfoByIdView(generics.RetrieveAPIView):
    queryset = Sleep.objects.all()
    serializer_class = SleepInfoSerializer
    lookup_field = 'sleep_id'


class PersonInfoListView(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonInfoSerializer


class PersonInfoView(generics.RetrieveAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonInfoSerializer
    lookup_field = 'person_id'


class SleepInfoAnalyticsView(generics.RetrieveAPIView):
    serializer_class = SleepInfoAnalyticsSerializer

    def get_object(self):
        person_id = self.kwargs['person_id']
        average_score = self.calculate_average_score(person_id)
        person_info = self.get_person_info(person_id)
        opinion_analytics = self.get_analytics(person_id)

        return {'person_info': person_info, 'average_score': average_score,
                'opinion_analytics': opinion_analytics}

    def calculate_average_score(self, person_id):
        average_score = Sleep.objects.filter(person_id=person_id).aggregate(
            Avg('sleep_score'))['sleep_score__avg']
        return average_score

    def get_person_info(self, person_id):
        person = Person.objects.filter(person_id=person_id).first()
        if person:
            serializer = PersonInfoSerializer(person)
            return serializer.data
        return {}

    def get_analytics(self, person_id):
        sleep_comments = Sleep.objects.filter(person_id=person_id).values_list(
            'sleep_comments', flat=True)
        return analyze_opinions(sleep_comments)


class AverageEnvironmentView(generics.RetrieveAPIView):
    serializer_class = AverageEnvironmentSerializer

    def get_object(self):
        person_id = self.kwargs.get('personId')
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')

        if person_id:
            weather_records = WeatherAPI.objects.filter(
                station__person_id=person_id)
            noise_records = Noise.objects.filter(station__person_id=person_id)
        elif lat and lon:
            weather_records = WeatherAPI.objects.filter(station__lat=lat,
                                                        station__lon=lon)
            noise_records = Noise.objects.filter(station__lat=lat,
                                                 station__lon=lon)
        else:
            return Response({
                'error': 'Provide either person ID or latitude and longitude.'},
                status=status.HTTP_400_BAD_REQUEST)

        if not weather_records.exists() or not noise_records.exists():
            return Response(
                {'error': 'No data found for the specified criteria.'},
                status=status.HTTP_404_NOT_FOUND)

        environment_data = {
            'noise_avg': noise_records.aggregate(Avg('noise'))[
                             'noise__avg'] or None,
            'temp_c_avg': weather_records.aggregate(Avg('temp_c'))[
                              'temp_c__avg'] or None,
            'precip_mm_avg': weather_records.aggregate(Avg('precip_mm'))[
                                 'precip_mm__avg'] or None,
            'humidity_avg': weather_records.aggregate(Avg('humidity'))[
                                'humidity__avg'] or None,
        }

        return environment_data
