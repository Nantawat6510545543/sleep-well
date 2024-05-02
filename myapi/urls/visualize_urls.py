from django.urls import path
from myapi import views

visualize_patterns = [
    path('', views.get_visualize_list_view, name='visualize-list-view'),
    path('gender/', views.GenderView.as_view(), name='gender-view'),
]
