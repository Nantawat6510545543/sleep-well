from django.urls import path

from myapi.views.app_views import get_visualize_list_view, get_sleep_visualize_view
from myapi.views.visualize_views import *

visualize_patterns = [
    path('', get_visualize_list_view, name='visualize-list-view'),
    path('gender/', GenderView.as_view(), name='gender-view'),
    path('age/', AgeView.as_view(), name='age-view'),
    path('height/', HeightView.as_view(), name='height-view'),
    path('weight/', WeightView.as_view(), name='weight-view'),
    path('sleep/', get_sleep_visualize_view, name='sleep-view'),
    path('sleep/<int:person_id>', SleepView.as_view(), name='sleep-detail')
]
