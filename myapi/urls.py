from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info/sleep/', views.SleepInfoListView.as_view(),
         name='sleep-info-list'),
    path('info/sleep/<int:sleep_id>/', views.SleepInfoByIdView.as_view(),
         name='sleep-info-id'),
    path('info/sleep/person/<int:person_id>/', views.SleepInfoView.as_view(),
         name='sleep-info-person'),
    path('info/person/', views.PersonInfoListView.as_view(),
         name='person-info-list'),
    path('info/person/<int:person_id>/', views.PersonInfoView.as_view(),
         name='person-info-id'),
    path('avgScore/sleep/<int:person_id>/',
         views.SleepInfoAnalyticsView.as_view(), name='average-score'),
    path('avgEnvironment/<int:person_id>/',
         views.AverageEnvironmentView.as_view(), name='average-environment'),
]
