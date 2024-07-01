from django.db import models


class WeatherV1(models.Model):
    date_w= models.DateField(max_length=200)
    time_w=models.TimeField(max_length=200)
    temperature = models.FloatField()
    humidity = models.FloatField()
    precipitation = models.FloatField()
    windspeed = models.FloatField()
    solar_rad = models.FloatField()
    solar_engy = models.FloatField()
    delta_t = models.FloatField()
    place= models.CharField(max_length=200)
    zipcode=models.IntegerField()
    def __str__(self):
        header=f"Date of Input : {self.date_w} Time of Input : {self.time_w}"
        return header

class OutputV1(models.Model):
    remark_text = models.CharField(max_length=200)
    avg_delta_t = models.    delta_t = models.FloatField()
    def __str__(self):
        return self.remark_text