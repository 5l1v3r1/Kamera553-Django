from django.db import models
from django.utils import timezone, dateformat
from datetime import datetime

import re

class camera(models.Model):
    cam_name=models.CharField(max_length=64, blank=False, null= False, verbose_name="Kamera Adı",unique=True)
    cam_url=models.CharField(max_length=256, blank=False, null= False, verbose_name="Kamera Url Adresi")
    owner_id=models.IntegerField(blank=False, null= False, default=-1 , verbose_name="Kullanıcı ID si")
    cam_image=models.BinaryField(null=True,verbose_name="Kamera Anlık Feed")
    cam_period=models.IntegerField(blank=False, null=False, verbose_name="Periyot",default=1)
    cam_alarmstatus=models.BooleanField(default=False,verbose_name="Alarm Durumu")
    cam_status=models.BooleanField(default=False,verbose_name="Kamerda Durumu")
    cam_ownermail=models.CharField(max_length=256, blank=False, null= False, verbose_name="Kamera Sahip Email")

class alertme(models.Model):
    a_start=models.TimeField(max_length=5,blank=False,null=False,verbose_name="Başlangıç Saati")
    a_end=models.TimeField(max_length=5,blank=False,null=False,verbose_name="Başlangıç Saati")
    a_status=models.BooleanField(default=True,verbose_name="Kamerda Alarm Durumu")
    alert_image=models.BinaryField(null=True,verbose_name="Kamera Alarm Görüntüsü/")

class reports(models.Model):
    r_insansay=models.IntegerField(blank=False,null=False,verbose_name="İnsan Sayısı")
    r_tarih = models.DateTimeField(default=datetime.now,verbose_name="Tarih")
    r_camid= models.IntegerField(blank=False, null= False, default=-1 , verbose_name="Kamera Id si")
    r_yakinsay=models.IntegerField(blank=False,null=False,verbose_name="Yakın Duran İnsan Sayısı")

# Create your models here.
