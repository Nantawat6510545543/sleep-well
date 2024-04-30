from django.urls import path
from myapi import views

visualize_patterns = [
    path('', views.get_visualize_view, name='visualize-view'),
    path('gender/', views.GenderCountView.as_view(), name='gender-count'),
]
