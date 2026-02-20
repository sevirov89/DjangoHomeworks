from django.urls import path
from django.contrib import admin

from .views import SensorListView, MeasurementUpdateView, SensorCreateAPIView, SensorDetailView

urlpatterns = [
    path('create_sensors/', SensorCreateAPIView.as_view()),
    path('update_sensors/<int:pk>/', SensorDetailView.as_view()),
    path('measurement/<int:pk>/', MeasurementUpdateView.as_view()),
    path('list_sensors/', SensorListView.as_view()),
    path('list_sensors/detail/<int:pk>/', SensorDetailView.as_view()),
]
