from django.shortcuts import render,redirect
from .models import camera,alertme,reports
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseNotAllowed,HttpResponseRedirect
from .forms import CameraForm,AlertForm
from django.http import JsonResponse
from django.contrib import  messages
from django.db import connection
import subprocess
import os
import shutil
from datetime import datetime
import locale

# Create your views here.


def showcams(request):
    if request.user.id:
        if request.method=="POST":
            Cam=CameraForm(request.POST)
            if Cam.is_valid():
             
                if Cam.cleaned_data.get("Durum")=="1":
                    a=""
                    camName=Cam.cleaned_data.get("camName")
                    camUrl=Cam.cleaned_data.get("camUrl")
                    newcam=camera()
                    newcam.cam_name=camName
                    newcam.cam_url=camUrl
                    newcam.owner_id=request.user.id
                    usermail=User.objects.filter(id=request.user.id).values()
                    for mail in usermail:
                        a=mail["email"]
                        
                        print(mail["email"])
                    newcam.cam_ownermail=a
                    newcam.save()
                    if camName == "islem":
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
                if Alert.cleaned_data.get("Durum")=="1":
                    alertcount=alertme.objects.count()
                    if alertcount==0:
                        a_start=Alert.cleaned_data.get("starttime")
                        a_end=Alert.cleaned_data.get("endtime")
                        newalert=alertme()
                        newalert.a_start=a_start
                        newalert.a_end=a_end
                        newalert.save()
                       
                        messages.info(request,"Kayıt Başarıyla Oluşturuldu")
                        camera.objects.update(cam_alarmstatus=True)
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
    if request.user.id:
        if request.method=="POST":
            alerts=alertme.objects.all()
            for alert in alerts:
            
                alertme.objects.get(id=alert.id).delete()
                camera.objects.update(cam_alarmstatus=False)
            return HttpResponseRedirect("/cams/alerts/")
        else:
            return  HttpResponseRedirect("/cams/alerts/")
    else:
       
        return  HttpResponseRedirect("/cams/alerts/")   

def on(request,camname):
    if request.user.id:
        if camname == "islem":
            fh = open("NUL","w")
            subprocess.Popen(['python.exe',f'C:/YoloV4/darknet/build/darknet/x64/{camname}.py',"C:/YoloV4"],stdout = fh, stderr = fh)
            camera.objects.filter(cam_name=camname).update(cam_status=True)
        return redirect("/cams/")
    else:
        return redirect("/")

def off(request,camname):
    if request.user.id:
        camera.objects.filter(cam_name=camname).update(cam_status=False)
        return redirect("/cams/")
    else:
        return redirect("/")

def delcam(request,camname):
    if request.user.id:
        camera.objects.filter(cam_name=camname).delete()
        os.remove(f"C:/YoloV4/darknet/build/darknet/x64/{camname}.py")
        return redirect("/cams/")
    else:
        return redirect("/")

def showreports(request):
    if request.user.id:
        return render(request,"reports/index.html")
    else:
        return redirect("/")

def activatealert(request):
    if request.user.id:
        alertme.objects.update(a_status=True)
        return redirect("/cams/alerts/")
    else:
        return redirect("/")

def get_data(request,type):
    locale.setlocale(locale.LC_ALL,"tr")
    cursor = connection.cursor()
    tarih = []
    insanavg = []
    yazi = ""
    if type == "1":
        cursor.execute(""" SELECT 
        to_timestamp(floor((extract('epoch' from r_tarih) / 60)) * 60)
        AT TIME ZONE 'UTC' as interval_alias,
        avg(r_insansay) as insan
        FROM "Kamera553_reports"
        GROUP BY interval_alias
        ORDER BY interval_alias """)
        veri = cursor.fetchall()
        for bomba in veri[-10:]:
            tarih.append(bomba[0].strftime("%d %m %Y %H:%M"))
            insanavg.append(int(bomba[1]))
        yazi = "1 Dakikaya Göre İnsan Yoğunluğu"
    elif type == "2":
        cursor.execute(""" SELECT 
        to_timestamp(floor((extract('epoch' from r_tarih) / 300)) * 300)
        AT TIME ZONE 'UTC' as interval_alias,
        avg(r_insansay) as insan
        FROM "Kamera553_reports"
        GROUP BY interval_alias
        ORDER BY interval_alias """)
        veri = cursor.fetchall()
        for bomba in veri[-10:]:
            tarih.append(bomba[0].strftime("%d %m %Y %H:%M"))
            insanavg.append(int(bomba[1]))
        yazi = "5 Dakikaya Göre İnsan Yoğunluğu"
    elif type == "3":
        cursor.execute(""" SELECT 
        to_timestamp(floor((extract('epoch' from r_tarih) / 900)) * 900)
        AT TIME ZONE 'UTC' as interval_alias,
        avg(r_insansay) as insan
        FROM "Kamera553_reports"
        GROUP BY interval_alias
        ORDER BY interval_alias """)
        veri = cursor.fetchall()
        for bomba in veri[-10:]:
            tarih.append(bomba[0].strftime("%d %m %Y %H:%M"))
            insanavg.append(int(bomba[1]))
        yazi = "15 Dakikaya Göre İnsan Yoğunluğu"
    elif type == "4":
        cursor.execute(""" SELECT 
        to_timestamp(floor((extract('epoch' from r_tarih) / 1800)) * 1800)
        AT TIME ZONE 'UTC' as interval_alias,
        avg(r_insansay) as insan
        FROM "Kamera553_reports"
        GROUP BY interval_alias
        ORDER BY interval_alias """)
        veri = cursor.fetchall()
        for bomba in veri[-10:]:
            tarih.append(bomba[0].strftime("%d %m %Y %H:%M"))
            insanavg.append(int(bomba[1]))
        yazi = "30 Dakikaya Göre İnsan Yoğunluğu"
    elif type == "5":
        cursor.execute(""" SELECT 
        to_timestamp(floor((extract('epoch' from r_tarih) / 3600)) * 3600)
        AT TIME ZONE 'UTC' as interval_alias,
        avg(r_insansay) as insan
        FROM "Kamera553_reports"
        GROUP BY interval_alias
        ORDER BY interval_alias """)
        veri = cursor.fetchall()
        for bomba in veri[-10:]:
            tarih.append(bomba[0].strftime("%d %m %Y %H:%M"))
            insanavg.append(int(bomba[1]))
        yazi = "1 Saate Göre İnsan Yoğunluğu"
    elif type == "6":
        cursor.execute(""" SELECT 
        to_timestamp(floor((extract('epoch' from r_tarih) / 86400)) * 86400)
        AT TIME ZONE 'UTC' as interval_alias,
        avg(r_insansay) as insan
        FROM "Kamera553_reports"
        GROUP BY interval_alias
        ORDER BY interval_alias """)
        veri = cursor.fetchall()
        for bomba in veri[-10:]:
            tarih.append(bomba[0].strftime("%d %m %Y %H:%M"))
            insanavg.append(int(bomba[1]))
        yazi = "1 Güne Göre İnsan Yoğunluğu"
    elif type == "7":
        cursor.execute(""" SELECT 
        to_timestamp(floor((extract('epoch' from r_tarih) / 2592000)) * 2592000)
        AT TIME ZONE 'UTC' as interval_alias,
        avg(r_insansay) as insan
        FROM "Kamera553_reports"
        GROUP BY interval_alias
        ORDER BY interval_alias """)
        veri = cursor.fetchall()
        for bomba in veri[-10:]:
            tarih.append(bomba[0].strftime("%d %m %Y %H:%M"))
            insanavg.append(int(bomba[1]))
        yazi = "1 Aya Göre İnsan Yoğunluğu"
    elif type == "8":
        cursor.execute(""" SELECT 
        to_timestamp(floor((extract('epoch' from r_tarih) / 15552000)) * 15552000)
        AT TIME ZONE 'UTC' as interval_alias,
        avg(r_insansay) as insan
        FROM "Kamera553_reports"
        GROUP BY interval_alias
        ORDER BY interval_alias """)
        veri = cursor.fetchall()
        for bomba in veri[-10:]:
            tarih.append(bomba[0].strftime("%d %m %Y %H:%M"))
            insanavg.append(int(bomba[1]))
        yazi = "6 Aya Göre İnsan Yoğunluğu"
    elif type == "9":
        cursor.execute(""" SELECT 
        to_timestamp(floor((extract('epoch' from r_tarih) / 62208000)) * 62208000)
        AT TIME ZONE 'UTC' as interval_alias,
        avg(r_insansay) as insan
        FROM "Kamera553_reports"
        GROUP BY interval_alias
        ORDER BY interval_alias """)
        veri = cursor.fetchall()
        for bomba in veri[-10:]:
            tarih.append(bomba[0].strftime("%d %m %Y %H:%M"))
            insanavg.append(int(bomba[1]))
        yazi = "1 Yıla Göre İnsan Yoğunluğu"
    else:
        cursor.execute(""" SELECT 
        to_timestamp(floor((extract('epoch' from r_tarih) / 900)) * 900)
        AT TIME ZONE 'UTC' as interval_alias,
        avg(r_insansay) as insan
        FROM "Kamera553_reports"
        GROUP BY interval_alias
        ORDER BY interval_alias """)
        veri = cursor.fetchall()
        for bomba in veri[-10:]:
            tarih.append(bomba[0].strftime("%d %m %Y %H:%M"))
            insanavg.append(int(bomba[1]))
        yazi = "30 Dakikaya Göre İnsan Yoğunluğu"
    data={
        'label_data':tarih,
        'human_data':insanavg,
        'label':yazi,
    }
    return JsonResponse(data)