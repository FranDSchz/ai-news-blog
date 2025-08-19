from django.urls import path
from .views import RegistroUsuario, LoginUsuario, perfil, logout_usuario
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

app_name = 'apps.usuarios' 
urlpatterns = [
    path('registrar/', RegistroUsuario.as_view(), name='registrar'),
    path('login/', LoginUsuario.as_view(), name='login'),
    path('logout/', logout_usuario, name='logout'),
    path('perfil/<int:pk>', perfil, name='perfil'),
]