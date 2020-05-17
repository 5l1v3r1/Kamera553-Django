from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from .models import User

def index(request):
    if (request.session.get('id')):
        userinf={"id":request.session.get('id'),"name":request.session.get('name'),"surname":request.session.get('surname'),"email":request.session.get('email')}
        return render(request,"index.html",userinf)
    else:
        return render(request,"index.html")


def KayitOl(request):
    return render(request,"kayit.html")

def Kayit(request):
    if request.method=="POST":
        result = User.checkattempt(request.POST.get('name'),request.POST.get('surname'),request.POST.get('mail'),request.POST.get('password1'),request.POST.get('password2'))
        if (isinstance(result,int)):
            yenikullanici = User(name = request.POST.get("name"),surname = request.POST.get("surname"),email = request.POST.get("mail"),password = request.POST.get("password1"))
            yenikullanici.save()
            return redirect('/')
           
        else:
            return render(request,"kayit.html",{"nameError":result["nameError"] , "surnameError":result["surnameError"],"mailError":result["mailError"],"passwordError":result["passwordError"]})
    else:
        return JsonResponse(0)

def GirisYap(request):
    if request.method=="POST":
        result=User.objects.filter(email = request.POST.get('email'),password=request.POST.get('password')).count()
        if(result>0):
            user=User.objects.filter(email = request.POST.get('email'),password=request.POST.get('password')).first()
            if (request.POST.get('hatir',False)):
                request.session['id']=user.id
                request.session['name']=user.name
                request.session['surname']=user.surname
                request.session['email']=user.email
                return redirect("/")
            else:
                return HttpResponse("Biz Seni Unutacaksak Napak Yeğen ??")
        
        else:
            return HttpResponse("BİR CİSİM YAKLAŞIYOR EFENDİM!")    


    
        
# Create your views here.
