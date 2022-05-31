from django.db import models

# Create your models here.

class Pariwisata(models.Model):
    id = models.IntegerField
    nama = models.CharField(max_length=200)
    kota = models.CharField(max_length=50)
    def __str__(self):
        return self.nama

class Tourism_place(models.Model):
    place_id = models.IntegerField(null=True)
    place_name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    longitude = models.CharField(max_length=60)
    latitude = models.CharField(max_length=60)
    price = models.IntegerField(null=True)
    rating = models.FloatField(null=True)

    def __str__(self):
        return self.place_name
