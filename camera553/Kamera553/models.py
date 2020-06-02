from django.db import models
import re
regex1="[\w\-]+"
regex2="^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$"

class camera(models.Model):
    cam_name=models.CharField(max_length=64, blank=False, null= False, verbose_name="Kamera Adı")
    cam_url=models.CharField(max_length=256, blank=False, null= False, verbose_name="Kamera Url Adresi")
    owner_id=models.IntegerField(blank=False, null= False, default=-1 , verbose_name="Kullanıcı ID si")


    def check_requirements(camname,camurl,ownerid):


        a={"camnameError":"","camurlError":""}
        if camname==None or  camname=="" or  camurl==None or camurl==""  :
            a["camnameError"]+="Kamera Adı Alanı Boş Geçilemez?"
            a["camurlError"]+="Kamera Adı Alanı Boş Geçilemez?"
            return a
           
        else:
            camname=camname.str()
            camurl=camurl.str()
            if not re.search(regex1,camname) :
                a["camnameError"]+="Kamera Adı İçin Geçersiz Karakter!"
            if  not re.search(regex2,camurl) :
                a["camurlError"]+="Kamera Adı İçin Geçersiz Karakter!"
            return a
# Create your models here.
