from django.db import models
import re

class camera(models.Model):
    cam_name=models.CharField(max_length=64, blank=False, null= False, verbose_name="Kamera Adı")
    cam_url=models.CharField(max_length=256, blank=False, null= False, verbose_name="Kamera Url Adresi")
    owner_id=models.IntegerField(blank=False, null= False, default=-1 , verbose_name="Kullanıcı ID si")



# Create your models here.
