from django.shortcuts import render
from Kamera553User.forms import LoginForm

def index(request):
    form = LoginForm()
    data = {
        'title': 'Anasayfa',
        'form': form
    }
    return render(request,'home/index.html',data)