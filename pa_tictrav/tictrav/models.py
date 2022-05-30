from django.db import models

# Create your models here.

class Pariwisata(models.Model):
    id = models.IntegerField
    nama = models.CharField(max_length=200)
    kota = models.CharField(max_length=50)

def __str__(self):
    return self.nama