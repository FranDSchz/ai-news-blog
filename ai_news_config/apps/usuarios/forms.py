from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario, MensajeContacto, Perfil
from django import forms
class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email']
class ContactoForm(forms.Form):
    nombre = forms.CharField(
        label=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe tu nombre'})
    )
    email = forms.EmailField(
        label=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
    )
    asunto = forms.CharField(
        label=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto del mensaje'})
    )
    mensaje = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe aquí tu mensaje'})
    )
        
class UsuarioUpdateForm(forms.ModelForm):
    # Formulario para actualizar datos del modelo Usuario (los que no son sensibles)
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email']

class PerfilUpdateForm(forms.ModelForm):
    # Formulario para actualizar datos del modelo Perfil
    class Meta:
        model = Perfil
        fields = ['biografia', 'imagen_perfil']