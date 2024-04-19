from django.db.models import Avg
from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import render

from .analytics import analyze_opinions
from .models import Sleep, Person, Weather, NoiseStation
from .serializers import SleepInfoSerializer, PersonInfoSerializer, \
    SleepInfoAnalyticsSerializer, AverageEnvironmentSerializer


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
