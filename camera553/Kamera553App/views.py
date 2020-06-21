from django.shortcuts import render
from Kamera553User.forms import LoginForm
from Kamera553.models import camera

def index(request):
    cameras=list(camera.objects.filter(owner_id=request.user.id).values())
    print(cameras)
    form = LoginForm()
    data = {
        'title': 'Anasayfa',
        'form': form,
        'cameras':cameras
    }
    return render(request,'home/index.html',data)