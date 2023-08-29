from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroUsuarioForm
from .models import *
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

# Create your views here.

def bienvenida(request):
    return render(request,'home/index.html')

@login_required
def home(request):
    return render(request,'home/home.html')


@login_required
def staffPage(request):
    lista_usuario = User.objects.all()
    return render(request,'home/restricted_page.html', {
        'lista_usuario' : lista_usuario
    })

@login_required
def mostrarUsuario(request):
    lista_usuario = User.objects.all()
    return render(request, 'home/mostrar_usuario.html', {
        'lista_usuario' : lista_usuario
    })

@login_required
def logout(request):
    logout(request)

def registro(request):
    if request.method == "POST":
        formulario_p = RegistroUsuarioForm(request.POST)
        if formulario_p.is_valid():
                user = formulario_p.save(commit=False)
                # Asegurarse de que la contraseña se encripte utilizando el método save() personalizado
                grupo_seleccionado = formulario_p.cleaned_data['tipo_usuario']
                if grupo_seleccionado == 'admin':
                    grupo = Group.objects.filter(name='admin').first()
                elif grupo_seleccionado == 'usuario_comun':
                    grupo = Group.objects.filter(name='usuario_comun').first()
                elif grupo_seleccionado == 'permission_manger':
                    grupo = Group.objects.filter(name='permission_manger').first()
                else:
                # Caso predeterminado: en caso de un valor inesperado
                    grupo = None
                user.save()
                if grupo:
                    user.groups.add(grupo)
                login(request, user) 
                #login(request, user)
                return redirect('blog')

        else:
            messages.error(request, "Hubo un error en el registro")
    formulario = RegistroUsuarioForm()
    return render(request, 'home/registro.html', {'formulario': formulario})


