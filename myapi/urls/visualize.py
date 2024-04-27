from django.urls import path
from myapi import views

visualize_patterns = [
    path('gender/', views.GenderCountView.as_view(), name='gender-count'),
]
