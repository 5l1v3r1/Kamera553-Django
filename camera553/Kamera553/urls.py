from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.showcams,name="show_cam"),
    path('alerts/',views.showalerts,name="show_alerts"),
    path('gorsel/<camid>/',views.kameragoster,name="kamera_izle"),
    path('vericek/<camid>/',views.resimverisi,name="kamera_live"),
    path('alerts/delalert',views.delAlert,name="Alert Silme"),
    path('off/<camname>/',views.off,name="Kamera Kapat"),
    path('on/<camname>/',views.on,name="Kamera Aç"),
    path('delcam/<camname>/',views.delcam,name="Kamera Sil"),
    path('reports/',views.showreports,name="Raporlar Sayfası")
]