from django.shortcuts import redirect, render

from myapi.views.api_views import PersonInfoListView, SleepInfoListView

def index(request):
    return render(request, 'myapi/index.html')

def get_visualize_list_view(request):
    return render(request, 'myapi/visualize_list.html')

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
