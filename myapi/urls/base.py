from django.urls import path, include
from myapi import views
from .info import info_patterns
from .visualize import visualize_patterns

urlpatterns = [
    path('', views.index, name='index'),
    path('info/', include(info_patterns)),
    path('visualize/', include(visualize_patterns)),
]
