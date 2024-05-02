from django.urls import path
from myapi.views import app_views

visualize_patterns = [
    path('', app_views.get_visualize_list_view, name='visualize-list-view'),
    path('gender/', app_views.GenderView.as_view(), name='gender-view'),
    path('age/', app_views.AgeView.as_view(), name='age-view'),
    path('height/', app_views.HeightView.as_view(), name='height-view'),
    path('weight/', app_views.WeightView.as_view(), name='weight-view'),
    path('sleep/', app_views.SleepView.as_view(), name='sleep-detail'),
    path('sleep/<int:person_id>', app_views.SleepView.as_view(), name='sleep-detail')
]
