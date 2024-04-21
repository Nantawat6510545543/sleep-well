from django.db.models import Avg
from django.views.generic import TemplateView
from rest_framework import generics
from django.shortcuts import render, get_object_or_404

from .analytics import analyze_opinions
from .models import Sleep, Person, Weather, Noise
from .serializers import SleepInfoSerializer, PersonInfoSerializer, \
    SleepInfoAnalyticsSerializer
from .utils import get_closest


def index(request):
    return render(request, 'myapi/index.html')


class GenderCountView(TemplateView):
    template_name = 'myapi/gender_visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['male_count'] = Person.objects.filter(sex='Male').count()
        context['female_count'] = Person.objects.filter(sex='Female').count()
        context['other_count'] = Person.objects.filter(sex='Other').count()
        return context


class SleepInfoListView(generics.ListAPIView):
    serializer_class = SleepInfoSerializer

    def get_queryset(self):
        sleeps = Sleep.objects.all()

        for sleep in sleeps:
            sleep.closest_weather = get_closest(sleep, Weather)
            sleep.closest_noise_station = get_closest(sleep, Noise)

        return sleeps


class SleepInfoByPersonView(generics.ListAPIView):
    serializer_class = SleepInfoSerializer

    def get_queryset(self):
        sleeps = Sleep.objects.filter(person_id=self.kwargs['person_id'])
        for sleep in sleeps:
            sleep.closest_weather = get_closest(sleep, Weather)
            sleep.closest_noise_station = get_closest(sleep, Noise)
        return sleeps


class SleepInfoByIdView(generics.RetrieveAPIView):
    serializer_class = SleepInfoSerializer

    def get_object(self):
        sleep = get_object_or_404(Sleep, sleep_id=self.kwargs['sleep_id'])
        sleep.closest_weather = get_closest(sleep, Weather)
        sleep.closest_noise_station = get_closest(sleep, Noise)
        return sleep


class PersonInfoListView(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonInfoSerializer


class PersonInfoView(PersonInfoListView):
    lookup_field = 'person_id'


class SleepInfoAnalyticsView(generics.RetrieveAPIView):
    serializer_class = SleepInfoAnalyticsSerializer

    def get_object(self):
        person_id = self.kwargs['person_id']
        person_info = self.get_person_info(person_id)

        sleep = Sleep.objects.filter(person_id=person_id)
        average_score = sleep.aggregate(Avg('sleep_score'))['sleep_score__avg']
        sleep_comments = sleep.values_list('sleep_comments', flat=True)
        opinion_analytics = analyze_opinions(sleep_comments)

        return {'person_info': person_info, 'average_score': average_score,
                'opinion_analytics': opinion_analytics}

    def get_person_info(self, person_id):
        person = Person.objects.filter(person_id=person_id)
        if person:
            serializer = PersonInfoSerializer(person)
            return serializer.data
        return {}
