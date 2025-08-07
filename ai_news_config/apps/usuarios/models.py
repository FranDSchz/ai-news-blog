from django.db import models
from django.contrib.auth.models import AbstractUser  #Agregue este models que trae un sistema de usuarios. 
# Create your models here.

class Usuario(AbstractUser):
    ROL_CHOICES = [ ('admin', 'Administrador'),
                   ('autor', 'Autor'), 
                   ('lector','Lector')]  #Roles . 
    
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='lector') 
    creacion = models.DateTimeField(auto_now_add= True)
    
    def __str__(self):
        return self.username
