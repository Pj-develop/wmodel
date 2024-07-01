from django.urls import path

from . import views
from .views import RULView,AnomalyView

app_name = "getweather"

# urlpatterns = [
#     path("", views.IndexView.as_view(), name="index"),
#     path("<int:pk>/", views.DetailView.as_view(), name="detail"),
#     path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
#     path("<int:question_id>/vote/", views.vote, name="vote"),
# ]

urlpatterns = [
    path("show_weather_data/", views.show_weather_data, name="show_weather_data"),
    path("", views.solidification, name="solidification"), 
    path("solidificationAPI/", views.solidificationAPI, name="solidificationAPI"),
    path("rul/", RULView.as_view(), name="rul"),
    path("anomaly/", AnomalyView.as_view(), name="anomaly"),
]
