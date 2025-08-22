from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, View
from django.contrib import messages
from .forms import RegistroUsuarioForm,ContactoForm, UsuarioUpdateForm, PerfilUpdateForm
from .models import Perfil, Usuario
from apps.noticias.models import Post, Comentario
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

class RegistroUsuario(CreateView):
    model = Usuario
    template_name = 'usuarios/register.html'
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('apps.usuarios:login')

    def form_valid(self, form):
        self.object = form.save()  
        messages.success(self.request, '¡Registro exitoso! Por favor, inicia sesión.')
        return redirect(self.get_success_url())
    
class LoginUsuario(LoginView):
    template_name = 'usuarios/login.html'

    def get_success_url(self):
        messages.success(self.request, f'¡Bienvenido de nuevo, {self.request.user.username}!')
        return super().get_success_url()
    

@login_required
def perfil(request,pk):
    perfil_a_ver = get_object_or_404(Perfil, pk=pk)
    usuario_a_ver = perfil_a_ver.usuario
    posts_usuario = Post.objects.filter(autor=usuario_a_ver, estado='publicado').order_by('-fecha_publicacion')
    comentarios_usuario = Comentario.objects.filter(usuario=usuario_a_ver).order_by('-fecha_creacion')

    context = {
        'perfil_a_ver': perfil_a_ver,
        'posts_usuario': posts_usuario,
        'comentarios_usuario': comentarios_usuario,
    }
    return render(request, 'usuarios/perfil.html', context)

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        # Pasamos la instancia del usuario y perfil actual a los formularios
        usuario_form = UsuarioUpdateForm(request.POST, instance=request.user)
        perfil_form = PerfilUpdateForm(request.POST, request.FILES, instance=request.user.perfil)

        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()
            perfil_form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado exitosamente!')
            # Redirigimos al perfil público del usuario
            return redirect('apps.usuarios:perfil', pk=request.user.perfil.pk)
    else:
        usuario_form = UsuarioUpdateForm(instance=request.user)
        perfil_form = PerfilUpdateForm(instance=request.user.perfil)

    context = {
        'usuario_form': usuario_form,
        'perfil_form': perfil_form
    }
    return render(request, 'usuarios/editar_perfil.html', context)


def logout_usuario(request):
    logout(request)
    messages.success(request, '¡Has cerrado sesión exitosamente!')
    return redirect('home')

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
            
            email_remitente = settings.DEFAULT_FROM_EMAIL
            email_destinatario = settings.EMAIL_ADMIN_CONTACTO
            try:
                send_mail(asunto, mensaje_email, email_remitente, [email_destinatario])
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