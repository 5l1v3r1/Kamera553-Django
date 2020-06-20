from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.showcams,name="show_cam"),
    path('alerts/',views.showalerts,name="show_alerts"),
    path('gorsel/',views.kameragoster,name="kamera_izle"),
    path('vericek/',views.resimverisi,name="hoppaabimeveri")
]