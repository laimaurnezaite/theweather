from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=255)
    geoname_id = models.IntegerField()
    state = models.CharField(max_length=255, default="")
    country = models.CharField(max_length=255)
    lon = models.FloatField()
    lat = models.FloatField()


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'cities'