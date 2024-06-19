from django.contrib import admin

from .models import WeatherV1, OutputV1

admin.site.register(WeatherV1)
admin.site.register(OutputV1)