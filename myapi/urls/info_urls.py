from django.urls import path, include, register_converter
from myapi import views, converters

register_converter(converters.FloatUrlParameterConverter, 'float')

info_patterns = [
    path('sleep/', include([
        path('', views.get_sleep_info_list_view, name='sleep-info-list'),
        path('<int:sleep_id>/', views.SleepInfoByIdView.as_view(), name='sleep-info-id'),
        path('person/<int:person_id>/', views.SleepInfoByPersonView.as_view(),
             name='sleep-info-person'),
        path("<float:lat>-<float:lon>/", views.SleepInfoByLocationView.as_view(),
             name='sleep-info-location-within-5-km'),
        path("<float:lat>-<float:lon>/range/<int:km>", views.SleepInfoByLocationView.as_view(),
             name='sleep-info-location-within-range'),
        path("date/", views.SleepInfoByDateView.as_view()),
    ])),

    path('person/', include([
        path('', views.get_person_info_list_view, name='person-info-list'),
        path('<int:person_id>/', views.PersonInfoView.as_view(), name='person-info-id'),
        path('<int:person_id>/sleep/', views.SleepInfoByPersonView.as_view(),
             name='sleep-info-person'),
        path('<int:person_id>/sleep-analytics/',
             views.SleepInfoAnalyticsByPersonView.as_view(), name='sleep-analytics-person'),
    ])),

    path('sleep-analytics/', include([
        path('', views.SleepInfoAnalyticsView.as_view(), name='sleep-analytics'),
        path('person/<int:person_id>/', views.SleepInfoAnalyticsByPersonView.as_view(),
             name='sleep-analytics-person'),
    ])),
]
