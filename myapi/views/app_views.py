from django.shortcuts import redirect, render

from myapi.predict import svm
from myapi.models import Person
from myapi.utils import get_analytics_data
from myapi.views.api_views import PersonInfoListView, SleepInfoListView


def index(request):
    return render(request, 'myapi/index.html')


def get_visualize_list_view(request):
    return render(request, 'myapi/visualize_list.html')


def model_view(request):
    data = [get_analytics_data(person.person_id) for person in Person.objects.all()]
    model, accuracy, matrix = svm(data)
    context = {
        "model": model,
        "conflict matrix": matrix,
        "accuracy": accuracy
    }
    return render(request, 'myapi/model_view.html',context)


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
