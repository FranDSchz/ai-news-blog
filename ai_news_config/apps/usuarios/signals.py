from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, Perfil

@receiver(post_save, sender=Usuario)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """
    Esta función se ejecuta cada vez que se guarda un objeto Usuario.
    Si el usuario acaba de ser CREADO (created=True), también se crea su perfil.
    """
    if created:
        Perfil.objects.create(usuario=instance)
    instance.perfil.save()