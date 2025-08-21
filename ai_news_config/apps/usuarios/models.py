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
    
class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="perfil")
    biografia = models.TextField(blank=True, null=True)
    imagen_perfil = models.ImageField(upload_to='imagenes_perfiles/', null=True, blank=True)

    def __str__(self):
        return f'Perfil de {self.usuario.username}'
    

class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha_enviado = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    def __str__(self):
        return f"Mensaje de {self.nombre} ({self.email}) sobre '{self.asunto}'"
    
    class Meta:
        verbose_name = "Mensaje de Contacto"
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ['-fecha_enviado']