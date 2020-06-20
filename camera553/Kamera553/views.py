from django.shortcuts import render,redirect
from .models import camera,alertme
from django.http import HttpResponse,HttpResponseNotAllowed
from .forms import CameraForm,AlertForm
from django.http import JsonResponse
from django.contrib import  messages
import xml.etree.cElementTree as ET
import os

# Create your views here.
def fetch_cam(owner_id,cam_id):
    print("fetch cam çalıştı")
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'output'))
    x=1
    images=[]
    reqfilename="{}-{}.xml".format(owner_id,cam_id)
    print("reqfile is: "+reqfilename)
    print(path+"/"+reqfilename)
    if os.path.exists(path+"/"+reqfilename):
                print("Girdi")
                openfile = ET.parse(path+"/"+reqfilename)
                root = openfile.getroot()
                for okuma in root.iter("code"):
                    images.append({"image"+str(x):okuma.text})
                    
                    x+=1
                print(images)
                return images
    


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
                    return redirect("/cams/")
                else:
                    messages.info(request,Cam.cleaned_data.get("Errors"))
                    cameras=camera.objects.filter(owner_id=request.user.id)
                    form=CameraForm()
                    
                    data={
                        "title":"Kamera Ekleme Sayfası",
                        "form":form,

                        "cameras":cameras
                    }
                    return render(request,'camera/index.html',data)
            else:
                cameras=camera.objects.filter(owner_id=request.user.id)
                data={
                    "title":"Kamera Ekleme Sayfası",
                    "form":Cam,

                    "cameras":cameras
                }
                return render(request,'camera/index.html',data)
        else:
            cameras=list(camera.objects.filter(owner_id=request.user.id).values())
            print(cameras)
            print(type(cameras))
            form=CameraForm()

            data={
                "title":"Kamera Ekleme Sayfası",
                "form":form,

                "cameras":cameras,

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
                    a_start=Alert.cleaned_data.get("a_start")
                    a_end=Alert.cleaned_data.get("a_end")
                    newalert=alertme()
                    newalert.a_start=a_start
                    newalert.a_end=a_end
                    newalert.save()
                    print("saved")
                    messages.info(request,"Kayıt Başarıyla Oluşturuldu")
                    return redirect("/alerts/")
                else:
                    messages.info(request,Alert.cleaned_data.get("Errors"))

                    
                    
                    data={
                        "title":"İnsan Alarmı Saati Ekleme Sayfası",
                        "form":alert,


                    }
                    return render(request,'alert/index.html',data)
        else:
                
            data={
                "title":"İnsan Alarmı Saati Ekleme Sayfası",
                "form":alert,


            }
            return render(request,'alert/index.html',data)
    else:
        return redirect("/")   

def kameragoster(request):
    return render(request, "camera/kameraizle.html")

def resimverisi(request):
    cameras= camera.objects.filter(owner_id=request.user.id).values()
    for deger in cameras:
        return HttpResponse(deger["cam_image"])


