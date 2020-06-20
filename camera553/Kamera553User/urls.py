from django.contrib import admin
from django.urls import path
from . import views

app_name="Kamera553User"
urlpatterns = [
    path('register/',views.register,name="register"),
    path('login/',views.loginUser,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('yayinla/',views.get_image,name="yayin")
]
