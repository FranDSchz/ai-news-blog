from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from .forms import RegistroUsuarioForm
from .models import Perfil

class RegistroUsuario(CreateView):
    template_name = 'usuarios/register.html'
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):

        self.object = form.save()
        
        Perfil.objects.create(usuario=self.object)
    
        messages.success(self.request, '¡Registro exitoso! Por favor, inicia sesión.')
        
        return redirect(self.get_success_url())


