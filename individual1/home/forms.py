from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=False)
    campos = (
        ('usuario_comun', 'Usuario'),
        ('permission_manger', 'Taller')
    )
    tipo_usuario = forms.ChoiceField(choices=campos)
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']