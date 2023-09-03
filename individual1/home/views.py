from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroUsuarioForm, PostForm
from .models import *
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
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
                if grupo_seleccionado == 'usuario_comun':
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

@method_decorator(login_required, name='dispatch')
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home/blog.html'
    context_object_name = 'context'

def PostCreateView(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Configura automáticamente el autor como el usuario actualmente autenticado
            form.instance.author = request.user
            form.save()
            return redirect('blog')  # Redirige a la página del blog después de crear la publicación
    else:
        form = PostForm()
    return render(request, 'home/crear_posteo.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'home/modificar_posteo.html'
    success_url = reverse_lazy('blog')

def is_staff_or_admin(user):
    return user.is_staff or user.is_superuser

@method_decorator(user_passes_test(is_staff_or_admin), name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog')

@login_required  # Mantén el decorador para usuarios autenticados
def new_status(request, id):
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        comment_text = request.POST.get('comment_text')
        post = Post.objects.get(pk=id)
        Comment.objects.create(post=post, author_name=author_name, text=comment_text)
    return redirect('blog')

