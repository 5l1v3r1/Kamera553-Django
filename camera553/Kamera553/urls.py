from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.showcams,name="show_cam"),

]