from .models import Categoria, Notificacion

def menu_categorias(request):
    """
    Este procesador de contexto agrega la lista de todas las categorías
    al contexto de cada plantilla.
    """
    categorias = Categoria.objects.all()
    return {'categorias': categorias}

def notificaciones_context(request):
    """
    Añade el número de notificaciones no leídas al contexto de todas las plantillas.
    """
    if request.user.is_authenticated:
        # Filtra las notificaciones del usuario logueado que no han sido leídas.
        count = Notificacion.objects.filter(usuario_destino=request.user, leida=False).count()
        return {'notificaciones_no_leidas': count}
    return {}