from django.contrib import admin
from .models import Post, Comentario, Categoria
from django.utils import timezone

# Register your models here.


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.action(description='Publicar posts seleccionados')
def publicar_posts(modeladmin, request, queryset):
    """
    Acción que cambia el estado de los posts a 'publicado' y asigna la fecha de publicación.
    """
    for post in queryset:
        if post.estado != 'publicado':
            post.publicar() # Usamos el método que creamos en el modelo

class PostAdmin(admin.ModelAdmin):
    # --- CAMBIO 1: Actualizamos los campos a mostrar en la lista ---
    # Añadimos 'estado' y 'fecha_publicacion'. 'categoria' se reemplaza por 'mostrar_categorias'
    list_display = ('titulo', 'autor', 'estado', 'fecha_creacion', 'fecha_publicacion', 'mostrar_categorias')
    search_fields = ('titulo', 'contenido')
    
    # --- CAMBIO 2: Filtros mejorados ---
    # Usamos 'categoria__nombre' para poder filtrar por el nombre de la categoría
    list_filter = ('estado', 'categoria__nombre', 'fecha_creacion', 'autor')
    
    ordering = ('-fecha_creacion','fecha_publicacion',)
    
    # --- CAMBIO 3: Widget amigable para el ManyToMany ---
    filter_horizontal = ('categoria',)
    
    # --- CAMBIO 4: Añadimos la nueva acción ---
    actions = [publicar_posts]
    
    # Hacemos que las fechas importantes no se puedan editar manualmente
    readonly_fields = ('fecha_creacion', 'actualizacion', 'fecha_publicacion')
    
    # Método para mostrar las categorías en la lista (ya que ManyToMany no se puede mostrar directamente)
    def mostrar_categorias(self, obj):
        return ", ".join([cat.nombre for cat in obj.categoria.all()])
    mostrar_categorias.short_description = 'Categorías'

    def contenido_resumido(self, obj):
        return obj.contenido[:50] + "..." if len(obj.contenido) > 50 else obj.contenido
    contenido_resumido.short_description = "Vista previa"

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('post', 'usuario', 'fecha_creacion', 'texto_corto')
    search_fields = ('texto',)
    list_filter = ('fecha_creacion', 'usuario')
    ordering = ('-fecha_creacion',)
    
    # Renombramos el método para mayor claridad
    def texto_corto(self, obj):
        return obj.texto[:40] + "...." if len(obj.texto) > 40 else obj.texto
    texto_corto.short_description = "Comentario"

# Registramos los modelos con sus clases de Admin personalizadas
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Categoria, CategoriaAdmin)