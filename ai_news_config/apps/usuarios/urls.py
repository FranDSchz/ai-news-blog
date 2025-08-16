from django.urls import path
from .views import RegistroUsuario, LoginUsuario, LogoutUsuario, perfil

app_name = 'apps.usuarios' 
urlpatterns = [
    path('registrar/', RegistroUsuario.as_view(), name='registrar'),
    path('login/', LoginUsuario.as_view(), name='login'),
    path('logout/', LogoutUsuario.as_view(), name='logout'),
    path('perfil/', perfil, name='perfil'),
]