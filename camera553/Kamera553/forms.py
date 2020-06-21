from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import  messages
from .models import camera
import re
regex1="[\w\-]+"


class CameraForm(forms.Form):
    camName = forms.CharField(max_length=64,label="Kamera Adı",required=True,
                               help_text='Kamera Adınızı Sadece "A-Z" "a-z" "0-9" "-" ve "_" Kullanarak Yazınız!',
                               widget=forms.TextInput(attrs={'class': 'form-control rounded-0'}))
    camUrl = forms.CharField(max_length=256,label="Kamera URL' si",required=True,
                                 help_text='Kamera Adresinizi "http://mycam12345.com" Şeklinde Yazınız',
                                 widget=forms.TextInput(attrs={'class': 'form-control rounded-0'}))


    def clean(self):
        cam_name=self.cleaned_data.get("camName")
        cam_url=self.cleaned_data.get("camUrl")
        cameracount=camera.objects.filter(cam_name=cam_name).count()
        print (cameracount)
        Errors=""
        g=0
        if cameracount==0:
            if cam_name==None or  cam_name=="" or  cam_url==None or cam_url==""  :
                Errors+="Kamera Adı Alanı Boş Geçilemez?\n"
                g+=1
            else:
                if not re.search(regex1,cam_name) :
                    Errors+="Kamera Adı İçin Geçersiz Karakter!\n"
                    g+=1
                
            if g>0:
                values={
                    "Errors":Errors,
                    "Durum":"0"
                }
                return values



            values = {
                "camName": cam_name,
                "camUrl": cam_url,
                "Durum":"1"
            }

            return values
        else:
            Errors+="Bu Ada Sahip Bir Kamera Daha Önce Eklenmiş!"
            values={
                "Errors":Errors,
                "Durum":"0"
            }
            return values



class AlertForm(forms.Form):
    a_start = forms.TimeField(label="Başlangıç Saati",required=True,
                               help_text='Saat:Dakika Şeklinde Giriş Yapınız',
                               widget=forms.TimeInput(attrs={'class': 'form-control rounded-0','placeholder':'Saat Seçin'}))
    a_end = forms.TimeField(label="Bitiş Saati",required=True,
                                help_text='Saat:Dakika Şeklinde Giriş Yapınız',
                                widget=forms.TimeInput(attrs={'class': 'form-control rounded-0','placeholder':'Saat Seçin'}))

    def clean(self):
        starttime=self.cleaned_data.get("a_start")
        endtime=self.cleaned_data.get("a_end")
        Errors=""
        g=0
        if starttime==None or  starttime=="" or  endtime==None or endtime==""  :
            Errors+="Saat:Dakika Formatını Doğru Girdiğinizden Emin olun\n"
            g+=1
        
            if g>0:
                values={
                    "Errors":Errors,
                    "Durum":"0"
                    
                }
                return values



        values = {
            "Durum":"1",
            "starttime":starttime,
            "endtime":endtime
        }

        return values
        