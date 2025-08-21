from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, View
from django.contrib import messages
from .forms import RegistroUsuarioForm,ContactoForm
from .models import Perfil
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

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
def perfil(request,pk):
    perfil = get_object_or_404(Perfil,pk=pk)
    context = {'perfil':perfil}
    return render(request, 'usuarios/perfil.html',context)

def logout_usuario(request):
 
    logout(request)
    messages.success(request, '¡Has cerrado sesión exitosamente!')
    return redirect('home')

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


def contacto(request):
    # Lógica para procesar el envío del formulario (POST)
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Si el formulario es válido, lo guardamos en la base de datos
            form.save()

            # Preparamos y enviamos el email de notificación
            asunto = f"Nuevo mensaje de contacto de: {form.cleaned_data['nombre']}"
            mensaje_email = f"""
            Has recibido un nuevo mensaje de contacto a través del blog.
            
            Nombre: {form.cleaned_data['nombre']}
            Email: {form.cleaned_data['email']}
            Asunto: {form.cleaned_data['asunto']}
            
            Para gestionar este mensaje, por favor, visita el panel de administración.
            """
            email_admin = 'francodamiansanchez10@gmail.com' # Cambia esto por tu email
            
            try:
                send_mail(asunto, mensaje_email, 'no-responder@miblog.com', [email_admin])
            except Exception as e:
                # Opcional: Manejar errores de envío de email
                print(f"Error al enviar email: {e}")

            # Mostramos un mensaje de éxito al usuario
            messages.success(request, '¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.')
            
            # Redirigimos a la misma página para evitar reenvíos del formulario
            return redirect('contacto')

    # Lógica para mostrar la página por primera vez (GET)
    else:
        initial_data = {}
        # Si el usuario está logueado, pre-rellenamos los campos
        if request.user.is_authenticated:
            initial_data['nombre'] = request.user.get_full_name() or request.user.username
            initial_data['email'] = request.user.email
        
        form = ContactoForm(initial=initial_data)

    context = {
        'form': form
    }
    return render(request, 'contacto.html', context)