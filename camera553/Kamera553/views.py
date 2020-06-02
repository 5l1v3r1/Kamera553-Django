from django.shortcuts import render
from .models import camera
from django.http import HttpResponse

def mainpage(request):
     if request.method == "POST":
            if request.user.is_authenticated():
                return HttpResponse("Working")


# Create your views here.
def fetch_cam(request):
        if request.method == "POST":
            if request.user.is_authenticated():
                #Standart==Username-CamID.xml
                return HttpResponse(open('.xml').read(), content_type='text/xml')

def showcams(request):
        if request.method=="POST":
            a=camera.check_requirements(request.POST.get("camName"),request.POST.get("camurlName"),request.user.id)
            if isinstance(a,dict):
                return render(request,'camera/index.html',a)
            else:
                return HttpResponse("pfff")
        
        else:
            if request.user.id:
                return render(request,'camera/index.html')

