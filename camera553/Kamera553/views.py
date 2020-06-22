from django.shortcuts import render,redirect
from .models import camera,alertme
from django.http import HttpResponse,HttpResponseNotAllowed,HttpResponseRedirect
from .forms import CameraForm,AlertForm
from django.http import JsonResponse
from django.contrib import  messages
import xml.etree.cElementTree as ET
import subprocess
import os
import shutil

# Create your views here.


def showcams(request):
    if request.user.id:
        if request.method=="POST":
            Cam=CameraForm(request.POST)
            if Cam.is_valid():
                print("kamera formu geçerli")
                if Cam.cleaned_data.get("Durum")=="1":
                    camName=Cam.cleaned_data.get("camName")
                    camUrl=Cam.cleaned_data.get("camUrl")
                    newcam=camera()
                    newcam.cam_name=camName
                    newcam.cam_url=camUrl
                    newcam.owner_id=request.user.id
                    newcam.save()
                    print("saved")
                    messages.info(request,"Kayıt Başarıyla Oluşturuldu")
                    dosyapath = "E:/Code/Python/Development/Kamera553-Django/camera553/static/important/dontopen/important.py"
                    hedefpath = f"C:/YoloV4/darknet/build/darknet/x64/{camName}.py"
                    shutil.copy(dosyapath,hedefpath)
                    return redirect("/cams/")
                else:
                    messages.info(request,Cam.cleaned_data.get("Errors"))
                    cameras=list(camera.objects.filter(owner_id=request.user.id).values())
                    form=CameraForm()
                    
                    data={
                        "title":"Kamera Ekleme Sayfası",
                        "form":form,
                        "cameras":cameras
                        
                    }
                    return render(request,'camera/index.html',data)
            else:
                cameras=list(camera.objects.filter(owner_id=request.user.id).values())

                data={
                    "title":"Kamera Ekleme Sayfası",
                    "form":Cam,
                    "cameras":cameras

                    
                }
                return render(request,'camera/index.html',data)
        else:
            cameras=list(camera.objects.filter(owner_id=request.user.id).values())
            
            form=CameraForm()

            data={
                "title":"Kamera Ekleme Sayfası",
                "form":form,
                "cameras":cameras

            }
            
            return render(request,'camera/index.html',data)

    else:
        return redirect("/")

def showalerts(request):
    if request.user.id:
        alert=AlertForm()
        if request.method=="POST":
            Alert=AlertForm(request.POST)
            
            if Alert.is_valid():
                print("kamera formu geçerli")
                if Alert.cleaned_data.get("Durum")=="1":
                    alertcount=alertme.objects.count()
                    if alertcount==0:
                        a_start=Alert.cleaned_data.get("starttime")
                        a_end=Alert.cleaned_data.get("endtime")
                        newalert=alertme()
                        newalert.a_start=a_start
                        newalert.a_end=a_end
                        newalert.save()
                        print("saved")
                        messages.info(request,"Kayıt Başarıyla Oluşturuldu")
                        return redirect("/cams/alerts/")
                    else:
                        messages.info(request,"Zaten Bir Alarmınız Mevcut!")   
                        return redirect("/cams/alerts/") 

            else:
                messages.info(request,Alert.cleaned_data.get("Errors"))
                
                    
                    
                data={
                    "title":"İnsan Alarmı Saati Ekleme Sayfası",
                    "form":alert,


                }
                return render(request,'alert/index.html',data)
        else:
            alertdata=list(alertme.objects.all().values())
            print(alertdata)
            if len(alertdata)==0:
                data={
                    "title":"İnsan Alarmı Saati Ekleme Sayfası",
                    "form":alert
                    
                
                }
            else:
                 data={
                "title":"İnsan Alarmı Saati Ekleme Sayfası",
                "alertdata":alertdata,
                
                
            }   
            return render(request,'alert/index.html',data)
    else:
        return redirect("/")   

def kameragoster(request,camid):
    if request.user.id:
        data = {
            'camid':camid
        }
        return render(request, "camera/kameraizle.html",data)
    else:
        return redirect("/")      

def resimverisi(request,camid):
    if request.user.id:
        if request.method=="GET":
            cameras= camera.objects.filter(owner_id=request.user.id).filter(id=int(camid)).values()
            for deger in cameras:
                return HttpResponse(deger["cam_image"])
    else:
        return redirect("/")

def delAlert(request):
    print("Ana view geldi")
    if request.user.id:
        print("User id geldi")
        if request.method=="POST":
            print("alertin postu çalıştı")
            alerts=alertme.objects.all()
            for alert in alerts:
                print(alert)
                alertme.objects.get(id=alert.id).delete()
            return HttpResponseRedirect("/cams/alerts/")
        else:
            return  HttpResponseRedirect("/cams/alerts/")
    else:
        print("user id gelmedi")
        return  HttpResponseRedirect("/cams/alerts/")   

def on(request,camname):
    fh = open("NUL","w")
    subprocess.Popen(['python.exe',f'C:/YoloV4/darknet/build/darknet/x64/{camname}.py',"C:/YoloV4"],stdout = fh, stderr = fh)
    camera.objects.filter(cam_name=camname).update(cam_status=True)
    return redirect("/cams/")


def off(request,camname):
    camera.objects.filter(cam_name=camname).update(cam_status=False)
    return redirect("/cams/")

def delcam(request,camname):
    camera.objects.filter(cam_name=camname).delete()
    os.remove(f"C:/YoloV4/darknet/build/darknet/x64/{camname}.py")
    return redirect("/cams/")

def showreports(request):
    if request.user.id:
        return render(request,"reports/index.html")
    else:
        return redirect("/")

def get_data(request,type):
    data = {
            'male_data': [41, 26, 57, 47, 49, 40, 67, 68, 24, 26],
            'female_data': [62, 39, 67, 33, 58, 67, 50, 48, 21, 30],
            'label_data': ['13-17', '18-24', '25-34', '34-44', '45-54', '55-64'],
    }
    if type == 1:
        data = {
            'male_data': [41, 26, 57, 47, 49, 40, 67, 68, 24, 26],
            'female_data': [62, 39, 67, 33, 58, 67, 50, 48, 21, 30],
            'label_data': ['13-17', '18-24', '25-34', '34-44', '45-54', '55-64'],
        }
    elif type == 2:
        data = {
            'male_data': [41, 26, 57, 47, 49, 40, 67, 68, 24, 26],
            'female_data': [62, 39, 67, 33, 58, 67, 50, 48, 21, 30],
            'label_data': ['13-17', '18-24', '25-34', '34-44', '45-54', '55-64'],
        }
    elif type == 3:
        data = {
            'male_data': [41, 26, 57, 47, 49, 40, 67, 68, 24, 26],
            'female_data': [62, 39, 67, 33, 58, 67, 50, 48, 21, 30],
            'label_data': ['13-17', '18-24', '25-34', '34-44', '45-54', '55-64'],
        }
    elif type == 4:
        data = {
            'male_data': [41, 26, 57, 47, 49, 40, 67, 68, 24, 26],
            'female_data': [62, 39, 67, 33, 58, 67, 50, 48, 21, 30],
            'label_data': ['13-17', '18-24', '25-34', '34-44', '45-54', '55-64'],
        }
    elif type == 5:
        data = {
            'male_data': [41, 26, 57, 47, 49, 40, 67, 68, 24, 26],
            'female_data': [62, 39, 67, 33, 58, 67, 50, 48, 21, 30],
            'label_data': ['13-17', '18-24', '25-34', '34-44', '45-54', '55-64'],
        }
    elif type == 6:
        data = {
            'male_data': [41, 26, 57, 47, 49, 40, 67, 68, 24, 26],
            'female_data': [62, 39, 67, 33, 58, 67, 50, 48, 21, 30],
            'label_data': ['13-17', '18-24', '25-34', '34-44', '45-54', '55-64'],
        }
    elif type == 7:
        data = {
            'male_data': [41, 26, 57, 47, 49, 40, 67, 68, 24, 26],
            'female_data': [62, 39, 67, 33, 58, 67, 50, 48, 21, 30],
            'label_data': ['13-17', '18-24', '25-34', '34-44', '45-54', '55-64'],
        }
    elif type == 8:
        data = {
            'male_data': [41, 26, 57, 47, 49, 40, 67, 68, 24, 26],
            'female_data': [62, 39, 67, 33, 58, 67, 50, 48, 21, 30],
            'label_data': ['13-17', '18-24', '25-34', '34-44', '45-54', '55-64'],
        }
    elif type == 9:
        data = {
            'male_data': [41, 26, 57, 47, 49, 40, 67, 68, 24, 26],
            'female_data': [62, 39, 67, 33, 58, 67, 50, 48, 21, 30],
            'label_data': ['13-17', '18-24', '25-34', '34-44', '45-54', '55-64'],
        }
    else:
        data = {
            'male_data': [41, 26, 57, 47, 49, 40, 67, 68, 24, 26],
            'female_data': [62, 39, 67, 33, 58, 67, 50, 48, 21, 30],
            'label_data': ['13-17', '18-24', '25-34', '34-44', '45-54', '55-64'],
        }
	
    return JsonResponse(data)