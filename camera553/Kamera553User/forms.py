from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User
import re
regex = '^[a-zA-Z0-9_.-]+@[a-zA-Z.]+?\.[a-zA-Z]{2,3}$'
regex2= '^[a-zA-Z ]+$'
regex3= '^[a-z0-9]+$'

class LoginForm(forms.Form):
    username = forms.CharField(max_length=32, label="Kullanıcı Adı", required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control rounded-0'}))
    password = forms.CharField(max_length=32, label="Şifre", required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control rounded-0'}))



class RegisterForm(forms.Form):
    username = forms.CharField(max_length=32,label="Kullanıcı Adı",required=True,
                               help_text="Kullanıcı adı boşluk içeremez maximum 32 karakter içerebilir.",
                               widget=forms.TextInput(attrs={'class': 'form-control rounded-0'}))
    first_name = forms.CharField(max_length=32,label="Ad",required=True,
                                 help_text="Adınız ve Soyadınız maximum 32 karakter içerebilir.",
                                 widget=forms.TextInput(attrs={'class': 'form-control rounded-0'}))
    last_name = forms.CharField(max_length=32,label="Soyad",required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control rounded-0'}))
    email = forms.EmailField(max_length=128,label="Email",required=True,
                             help_text="Email adresinizi kimseyle paylaşmamanızı öneririz",
                             widget=forms.EmailInput(attrs={'class': 'form-control rounded-0'}))
    password = forms.CharField(max_length=16,label= "Parola",required=True,
                               help_text="Paralonız en az 8 karakter en fazla 32 karakter olmalıdır",
                               widget=forms.PasswordInput(attrs={'class': 'form-control rounded-0'}))
    password2 = forms.CharField(max_length=16, label="Parola Tekrarı",required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control rounded-0'}))

    def clean(self):
        errors = []
        g = 0
        username = self.cleaned_data.get("username")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if first_name == "" or email == "" or last_name == "" or password == "" or password2 == "":
            errors.append(ValidationError("Lütfen alanları doldurun!"))
            g += 1
        if User.objects.filter(username=username).count()>0:
            errors.append(ValidationError("Kullanıcı adı kullanılıyor!"))
            g += 1
        if User.objects.filter(email=email).count()>0:
            errors.append(ValidationError("Mail adresi kullanılıyor!"))
            g += 1
        if password and password2 and password != password2:
            errors.append(ValidationError("Parolalar eşleşmiyor!"))
            g += 1
        if len(password) < 8 or len(password) > 32:
            errors.append(ValidationError("Şifreniz en az 8 en fazla 32 karakterden oluşabilir!"))
            g += 1
        if not re.search('',password) or re.search(' ',username):
            errors.append(ValidationError("Şifreniz ve kullanıcı adı boşluk içeremez!"))
            g += 1
        if not re.search(regex2,first_name) and re.search(regex2,last_name):
            errors.append(ValidationError("Adınız ve Soyadınız sadece harf içerebilir!"))
            g += 1
        if not re.search(regex3,username):
            errors.append(ValidationError("Kullanıcı adınız sadece küçük harf ve sayılar içerebilir!"))
            g+=1
        if not re.search(regex,email):
            errors.append(ValidationError("Email adresinizi doğru girdiğinizden emin olun!"))
            g += 1

        if(g > 0 ):
            raise ValidationError(errors)

        values = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }

        return values