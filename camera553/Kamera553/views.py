from django.shortcuts import render,redirect
from .models import camera
from django.http import HttpResponse
from .forms import CameraForm
from django.contrib import  messages

# Create your views here.
def fetch_cam(request):
        if request.method == "POST":
            if request.user.is_authenticated():
                #Standart==Username-CamID.xml
                return HttpResponse(open('.xml').read(), content_type='text/xml')

def showcams(request):
    if request.user.id:
        if request.method=="POST":
            Cam=CameraForm(request.POST)
            if Cam.is_valid():
                if Cam.cleaned_data.get("Durum")==1:
                    camName=Cam.cleaned_data.get("camName")
                    camUrl=Cam.cleaned_data.get("camUrl")
                    newcam=camera()
                    newcam.cam_name=camName
                    newcam.cam_url=camUrl
                    newcam.owner_id=request.user.id
                    newcam.save()
                    messages.info(request,"Kayıt Başarıyla Oluşturuldu")
                    return redirect("/cams/")
                else:
                    messages.info(request,Cam.cleaned_data.get("Errors"))
                    form=CameraForm()
                    data={
                        "title":"Kamera Ekleme Sayfası",
                        "form":form
                    }
                    return render(request,'camera/index.html',data)
            else:
                data={
                    "title":"Kamera Ekleme Sayfası",
                    "form":Cam
                }
                return render(request,'camera/index.html',data)
        else:
            form=CameraForm()
            data={
                "title":"Kamera Ekleme Sayfası",
                "form":form
            }
            return render(request,'camera/index.html',data)

    else:
        return redirect("/")

