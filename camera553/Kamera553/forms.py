from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import  messages
import re
regex1="[\w\-]+"
regex2="^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$"


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
        Errors=""
        g=0
        if cam_name==None or  cam_name=="" or  cam_url==None or cam_url==""  :
            Errors+="Kamera Adı Alanı Boş Geçilemez?\n"
            g+=1
        else:
            if not re.search(regex1,cam_name) :
                Errors+="Kamera Adı İçin Geçersiz Karakter!\n"
                g+=1
            if  not re.search(regex2,cam_url) :
                Errors+="Kamera URL İçin Geçersiz Karakter!\n"
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