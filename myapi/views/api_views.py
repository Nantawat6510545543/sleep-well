from django.db.models import Avg
from django.views.generic import TemplateView
from rest_framework import generics
from django.shortcuts import get_object_or_404

from myapi.analytics import analyze_opinions
from myapi.models import Sleep, Person, Weather, Noise
from myapi.serializers import SleepInfoSerializer, PersonInfoSerializer, \
    SleepInfoAnalyticsSerializer
from myapi.utils import get_closest, get_environments


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


class PersonInfoView(generics.RetrieveAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonInfoSerializer
    lookup_field = 'person_id'


class SleepInfoAnalyticsView(generics.RetrieveAPIView):
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
