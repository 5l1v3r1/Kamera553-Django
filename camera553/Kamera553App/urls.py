from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="home"),
    path('user/',include("Kamera553User.urls")),
    path('cams/',include("Kamera553.urls")),
]
