from django.db import models
from django.conf import settings 

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Post(models.Model):
    ESTADO_CHOICE = [
        ('publicado', 'Publicado'),
        ('borrador', 'Borrador'),
    ]
    autor = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=225)
    contenido = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    imagen= models.ImageField(
    upload_to='imagenes_noticias', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    actualizacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICE, default='borrador')
    
    def __str__(self):
        return self.titulo
    
class Comentario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.post.titulo}"