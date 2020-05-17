from django.db import models
from django.shortcuts import render
import re
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
regex2='^[a-zA-Z ]+$'
regex3='^\S+/'





class User(models.Model):
    id=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name=models.CharField(max_length=64,verbose_name="Ad")
    surname=models.CharField(max_length=64,verbose_name="Soyad")
    email=models.EmailField(max_length=128,verbose_name="Eposta")
    password=models.CharField(max_length=64,verbose_name="Şifre")

    def checkattempt(name,surname,email,password1,password2):
       name=name.strip()
       surname=surname.strip()
       email=email.strip()
       password1=password1.strip()
       password2=password2.strip()
       g=0
       num_results = User.objects.filter(email = email).count()

       a={"nameError":"","surnameError":"","mailError":"","passwordError":""}
       if (name==""):
           a["nameError"]+="\nAd Boş Geçilemez!"
           g+=1
       if (surname==""):
           a["surnameError"]+="\nSoyad Boş Geçilemez!"
           g+=1
       if (email==""):
           a["emailError"]+="\nEposta Boş Geçilemez!"  
           g+=1
       if (re.search(regex3,password1)):
           a["emailError"]+="\nŞifre İçin Geçersiz Karakter!"
       if (password1=="" or password2==""):
           a["passwordError"]+="\nŞifre Alanı Boş Geçilemez!"  
           g+=1
       if ((re.search(regex2,name))==False ):
           a["nameError"]+="\nAdınız sadece harf içerebilir." + name
           g+=1
       if ((re.search(regex2,surname))==False):
           a["surnameError"]+="\nSoyadınız sadece harf içerebilir."
           g+=1    
       if (re.search(regex,email)==False):
           a["mailError"]+="\nLütfen doğru düzgün mail adresini giriniz.(example@domain.com)"
           g+=1
       if (num_results>0):
           a["mailError"]+="\nPosta Adresi Daha Önce Kullanılmış!"
           g+=1
       if (password1!=password2):
           a["nameError"]+="\nŞifreniz eşleşmiyor!"
           g+=1
       if (g!=0):
            return a
       else:
            return g

            
def __str__(self):
    return self.email + " || " + self.name + " " + self.surname




# Create your models here.
