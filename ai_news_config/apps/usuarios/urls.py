from django.urls import path,reverse_lazy
from .views import RegistroUsuario, LoginUsuario, perfil, logout_usuario,editar_perfil
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
app_name = 'apps.usuarios' 
urlpatterns = [
    path('registrar/', RegistroUsuario.as_view(), name='registrar'),
    path('login/', LoginUsuario.as_view(), name='login'),
    path('logout/', logout_usuario, name='logout'),
    path('perfil/<int:pk>', perfil, name='perfil'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='usuarios/registration/password_reset_form.html',
             email_template_name='usuarios/registration/password_reset_email.html',
             subject_template_name='usuarios/registration/password_reset_subject.txt',
             success_url=reverse_lazy('apps.usuarios:password_reset_done')),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='usuarios/registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='usuarios/registration/password_reset_confirm.html',
             success_url=reverse_lazy('apps.usuarios:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='usuarios/registration/password_reset_complete.html'),
         name='password_reset_complete'),
]