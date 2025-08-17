from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, View
from django.contrib import messages
from .forms import RegistroUsuarioForm
from .models import Perfil
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

class RegistroUsuario(CreateView):
    template_name = 'usuarios/register.html'
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save()  
        Perfil.objects.create(usuario=self.object)
        messages.success(self.request, '¡Registro exitoso! Por favor, inicia sesión.')
        return redirect(self.get_success_url())
    
class LoginUsuario(LoginView):
    template_name = 'usuarios/login.html'

    def get_success_url(self):
        messages.success(self.request, f'¡Bienvenido de nuevo, {self.request.user.username}!')
        return super().get_success_url()
    

@login_required
def perfil(request):
    return render(request, 'usuarios/perfil.html')

def logout_usuario(request):
 
    logout(request)
    messages.success(request, '¡Has cerrado sesión exitosamente!')
    return redirect('apps.usuarios:login')

def register(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                grupo_miembro = Group.objects.get(name='Miembro')
                user.groups.add(grupo_miembro)
            except Group.DoesNotExist:
                pass
            messages.success(request, '¡Registro exitoso! Por favor, inicia sesión.')
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/register.html', {'form': form})
