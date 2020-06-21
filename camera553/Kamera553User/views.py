from django.shortcuts import render,redirect
from django.http import  HttpResponse,StreamingHttpResponse
from .forms import RegisterForm,LoginForm
from django.contrib import  messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            newUser = User(username=username,first_name=first_name,last_name=last_name,email=email)
            newUser.set_password(password)
            newUser.save()
            login(request,newUser)
            return redirect('/')
        else:
            data = {
                'title': 'Kayıt Ol',
                'form': form
            }
            return render(request, "register/index.html", data)

    else:
        form = RegisterForm()
        data = {
            'title': 'Kayıt Ol',
            'form': form
        }
        return render(request,"register/index.html",data)

def loginUser(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        data = {
            'title': 'Anasayfa',
            'form': form
        }
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username,password=password)
            if user is None:
                messages.info(request,"Kullanıcı Adı veya Parola Hatalı")
                return render(request,"home/index.html",data)
            login(request,user)
            return redirect('/')
        else:
            messages.info(request, "Kullanıcı Adı veya Parola Hatalı")
            return render(request, "home/index.html", data)
    else:
        return redirect('/')

def logoutUser(request):
    logout(request)
    return redirect('/')


def get_image(request):
    return render(request, "camera/yayin.html")

