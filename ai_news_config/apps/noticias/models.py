# ai_news_config/apps/noticias/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

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
    categoria = models.ManyToManyField(Categoria, related_name='posts')
    imagen = models.ImageField(upload_to='imagenes_noticias', blank=True, null=True)
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
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comentarios")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
# Al final de ai_news_config/apps/noticias/models.py

class Video(models.Model):
    titulo = models.CharField(max_length=225)
    descripcion = models.TextField()
    # Usamos un campo ForeignKey para re-utilizar nuestro modelo Categoria.
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    # Aquí el editor pegará la URL normal de YouTube (ej: https://www.youtube.com/watch?v=...)
    url_video = models.URLField(max_length=200, help_text="Pega la URL del video de YouTube aquí")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    @property
    def embed_url(self):
        """
        Esta propiedad transforma la URL normal de YouTube a la versión "embed"
        que necesita el <iframe>. Es una forma limpia y reutilizable de hacerlo.
        """
        if "watch?v=" in self.url_video:
            video_id = self.url_video.split('watch?v=')[-1]
            return f"https://www.youtube.com/embed/{video_id}"
        # Podríamos añadir más lógica para otros tipos de URLs de YouTube si fuera necesario
        return self.url_video # Devuelve la URL original si no es el formato esperado