from django.urls import path

from myapi.views import *

visualize_patterns = [
    path('', get_visualize_list_view, name='visualize-list-view'),
    path('gender/', GenderView.as_view(), name='gender-view'),
    path('age/', AgeView.as_view(), name='age-view'),
    path('height/', HeightView.as_view(), name='height-view'),
    path('weight/', WeightView.as_view(), name='weight-view'),
    path('sleep-analytics/', SleepAnalyticsView.as_view(), name='sleep-analytics-view'),
    path('temp-c/', TempCView.as_view(), name='temp-c-view'),
    path('condition-text/', ConditionTextView.as_view(), name='condition-text-view'),
    path('precip-mm/', PrecipMMView.as_view(), name='precip-mm-view'),
    path('humidity/', HumidityView.as_view(), name='humidity-view'),
    path('noise/', NoiseView.as_view(), name='noise-view'),
    path('sleep-duration-vs-sleep-score/', SleepDurationVSSleepScoreView.as_view(), name='sleep-duration-vs-sleep-score'),

    path('sleep/', get_sleep_visualize_view, name='sleep-view'),
    path('sleep/<int:person_id>', SleepView.as_view(), name='sleep-detail'),
]
