from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("show_weather_data/", views.show_weather_data, name="show_weather_data"),
]