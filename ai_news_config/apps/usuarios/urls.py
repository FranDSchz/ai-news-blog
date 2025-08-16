from django.urls import path
from .views import RegistroUsuario

app_name = 'apps.usuarios' 
urlpatterns = [
    path('registrar/', RegistroUsuario.as_view(), name='registrar'),
]