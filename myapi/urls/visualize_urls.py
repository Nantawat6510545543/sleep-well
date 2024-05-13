from django.urls import path

from myapi.views import *

visualize_patterns = [
    path('', get_visualize_list_view, name='visualize-list-view'),

    # Person Visualization
    path('gender/', GenderView.as_view(), name='gender-view'),
    path('age/', AgeView.as_view(), name='age-view'),
    path('height/', HeightView.as_view(), name='height-view'),
    path('weight/', WeightView.as_view(), name='weight-view'),

    # Sleep Visualization
    path('sleep-analytics/', SleepAnalyticsView.as_view(), name='sleep-analytics-view'),

    # Environment Visualization
    path('temp-c/', TempCView.as_view(), name='temp-c-view'),
    path('condition-text/', ConditionTextView.as_view(), name='condition-text-view'),
    path('precip-mm/', PrecipMMView.as_view(), name='precip-mm-view'),
    path('humidity/', HumidityView.as_view(), name='humidity-view'),
    path('noise/', NoiseView.as_view(), name='noise-view'),

    # Comparison Visualization
    path('sleep-duration-vs-sleep-score/', SleepDurationVSSleepScoreView.as_view(), name='sleep-duration-vs-sleep-score'),

    path('sleep-duration-vs-temp-c/', SleepDurationVSTempCView.as_view(), name='sleep-duration-vs-temp-c'),
    path('sleep-duration-vs-precip-mm/', SleepDurationVSPrecipMMView.as_view(), name='sleep-duration-vs-precip-mm'),
    path('sleep-duration-vs-humidity/', SleepDurationVSHumidityView.as_view(), name='sleep-duration-vs-humidity'),
    path('sleep-duration-vs-noise/', SleepDurationVSNoiseView.as_view(), name='sleep-duration-vs-noise'),

    path('sleep-score-vs-temp-c/', SleepScoreVSTempCView.as_view(), name='sleep-score-vs-temp-c'),
    path('sleep-score-vs-precip-mm/', SleepScoreVSPrecipMMView.as_view(), name='sleep-score-vs-precip-mm'),
    path('sleep-score-vs-humidity/', SleepScoreVSHumidityView.as_view(), name='sleep-score-vs-humidity'),
    path('sleep-score-vs-noise/', SleepScoreVSNoiseView.as_view(), name='sleep-score-vs-noise'),

    path('sleep/', get_sleep_visualize_view, name='sleep-view'),
    path('sleep/<int:person_id>', SleepView.as_view(), name='sleep-detail'),
]
