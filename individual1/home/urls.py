from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import *

urlpatterns = [
    path('', views.bienvenida, name='index'),
    path('registro/', views.registro, name='registro'),
    path('mostrarUsuario/', views.mostrarUsuario, name='mostrarUsuario'),
    path('home/', views.home, name='home'),
    path('restricted_page/', views.staffPage, name='restricted_page'),
    path('crear_posteo/', views.PostCreateView, name='crear_posteo'),
    path('modificar_posteo/<pk>/', PostUpdateView.as_view(), name='modificar_posteo'),
    path('eliminar_posteo/<pk>/', PostDeleteView.as_view(), name='eliminar_posteo'),
    path('new_status/<id>/', views.new_status, name='new_status'),
    path('blog/', PostListView.as_view(), name='blog'),
]