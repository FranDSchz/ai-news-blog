# ai_news_config/apps/noticias/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comentario, Notificacion, Post
from django.contrib.auth.models import User

@receiver(post_save, sender=Comentario)
def crear_notificacion_comentario(sender, instance, created, **kwargs):
    """
    Crea una notificación cuando se guarda un nuevo comentario.
    """
    # 'created' es un booleano. Si es True, el comentario es nuevo.
    if created:
        # 'instance' es el objeto Comentario que se acaba de guardar.
        post = instance.post
        autor_post = post.autor
        comentador = instance.usuario

        # Evitamos que el autor se notifique a sí mismo
        if autor_post != comentador:
            mensaje = f"'{comentador.username}' ha comentado en tu post: '{post.titulo}'"
            
            Notificacion.objects.create(
                usuario_destino=autor_post,
                mensaje=mensaje,
                # Podrías agregar un campo en tu modelo Notificacion para enlazar al post
                # post_relacionado=post 
            )