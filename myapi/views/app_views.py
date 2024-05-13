import json

from django.shortcuts import redirect, render
from rest_framework.renderers import JSONRenderer

from myapi.predict import linear
from myapi.models import Sleep, Weather, Noise, Person
from myapi.utils import get_closest_station
from myapi.views.api_views import PersonInfoListView, SleepInfoListView
from myapi.serializers import SleepTrainSerializer


def index(request):
    return render(request, 'myapi/index.html')


def get_visualize_list_view(request):
    return render(request, 'myapi/visualize_list.html')


def model_view(request):
    sleeps = Sleep.objects.all()
    for sleep in sleeps:
        sleep.person = Person.objects.get(person_id=sleep.person_id)
        sleep.closest_weather = get_closest_station(sleep, Weather)
        sleep.closest_noise_station = get_closest_station(sleep, Noise)

    serializer = SleepTrainSerializer(sleeps, many=True)
    json_data = JSONRenderer().render(serializer.data)
    decoded_data = json.loads(json_data)

    args = {'context': linear(decoded_data)}
    return render(request, 'myapi/model_view.html', args)


# Fix for query parameters (?person_id=)
def get_person_info_list_view(request):
    person_id = request.GET.get('person_id')

    if person_id:
        return redirect('person-info-id', person_id=person_id)
    else:
        return PersonInfoListView.as_view()(request)


# Fix for query parameters (?sleep_id=)
def get_sleep_info_list_view(request):
    sleep_id = request.GET.get('sleep_id')

    if sleep_id:
        return redirect('sleep-info-id', sleep_id=sleep_id)
    else:
        return SleepInfoListView.as_view()(request)


# Fix for query parameters in sleep visualize view
def get_sleep_visualize_view(request):
    person_id = request.GET.get('person_id')
    if person_id:
        return redirect('sleep-detail', person_id=person_id)
    else:
        return render(request, 'myapi/sleep_visualize.html')
