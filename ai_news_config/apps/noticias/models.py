# ai_news_config/apps/noticias/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone # Asegúrate de que esto esté importado

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Post(models.Model):
    ESTADO_CHOICES = [
        ('publicado', 'Publicado'),
        ('borrador', 'Borrador'),
    ]
    
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=225)
    contenido = models.TextField()
    
    # --- VERIFICA ESTA LÍNEA ---
    categoria = models.ManyToManyField(Categoria, related_name='posts')
    
    imagen = models.ImageField(upload_to='imagenes_noticias', blank=True, null=True)
    
    # --- Y VERIFICA ESTAS LÍNEAS ---
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    actualizacion = models.DateTimeField(auto_now=True)
    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='borrador')
    
    def __str__(self):
        return self.titulo
    
    def publicar(self):
        self.estado = 'publicado'
        self.fecha_publicacion = timezone.now()
        self.save()

class Comentario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.autor.username} en {self.post.titulo}"