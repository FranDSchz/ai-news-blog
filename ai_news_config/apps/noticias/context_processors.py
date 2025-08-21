from .models import Categoria 

def menu_categorias(request):
    """
    Este procesador de contexto agrega la lista de todas las categorías
    al contexto de cada plantilla.
    """
    categorias = Categoria.objects.all()
    return {'categorias': categorias}