from django.db import models


class WeatherV1(models.Model):
    date_w= models.DateField(max_length=200)
    time_w=models.TimeField(max_length=200)
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    precipitation = models.IntegerField()
    windspeed = models.IntegerField()
    solar_rad = models.IntegerField()
    solar_engy = models.IntegerField()
    delta_t = models.IntegerField()
    place= models.CharField(max_length=200)
    zipcode=models.IntegerField()
    def __str__(self):
        return self.date_w


class OutputV1(models.Model):
    remark_text = models.CharField(max_length=200)
    avg_delta_t = models.IntegerField(default=0)
    def __str__(self):
        return self.remark_text