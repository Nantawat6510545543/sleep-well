from django.urls import path, include
from myapi import views

info_patterns = [
    path('sleep/', include([
        path('', views.SleepInfoListView.as_view(), name='sleep-info-list'),
        path('<int:sleep_id>/', views.SleepInfoByIdView.as_view(), name='sleep-info-id'),
        path('person/<int:person_id>/', views.SleepInfoByPersonView.as_view(),
             name='sleep-info-person'),
    ])),

    path('person/', include([
        path('', views.PersonInfoListView.as_view(), name='person-info-list'),
        path('<int:person_id>/', views.PersonInfoView.as_view(), name='person-info-id'),
        path('<int:person_id>/sleep/', views.SleepInfoByPersonView.as_view(),
             name='sleep-info-person'),
        path('<int:person_id>/sleep-analytics/',
             views.SleepInfoAnalyticsViewByPerson.as_view(), name='sleep-analytics-person'),
    ])),

    path('sleep-analytics/', include([
        path('', views.SleepInfoAnalyticsView.as_view(), name='sleep-analytics'),
        path('person/<int:person_id>/', views.SleepInfoAnalyticsViewByPerson.as_view(),
             name='sleep-analytics-person'),
    ])),
]
