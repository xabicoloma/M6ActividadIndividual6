from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import *

urlpatterns = [
    path('', views.bienvenida, name='blog'),
    path('registro/', views.registro, name='registro'),
    path('mostrarUsuario/', mostrarUsuario, name='mostrarUsuario'),
    path('home/', views.home, name='home'),
    path('restricted_page/', views.staffPage, name='restricted_page'),
]