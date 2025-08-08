from django.contrib import admin
from .models import Post, Comentario, Categoria



# Register your models here.


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'fecha_creacion', 'contenido_resumido')
    search_fields = ('titulo', 'contenido')
    list_filter = ('categoria', 'fecha_creacion', 'autor')
    ordering = ('-fecha_creacion',)
    readonly_fields = ('fecha_creacion',)
    
    def contenido_resumido(self, obj):
        return obj.contenido[:50] + "..." if len(obj.contenido) > 50 else obj.contenido
    contenido_resumido.short_description = "Vista previa"
    

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('post', 'usuario', 'fecha_creacion', 'contenido_corto')
    search_fields = ('contenido',)
    list_filter = ('fecha_creacion', 'usuario')
    ordering = ('-fecha_creacion',)
    
    
    def contenido_corto(self, obj):
        return obj.contenido[:40] + "...." if len(obj.contenido) > 40 else obj.contenido
    contenido_corto.short_description = "Comentario"


admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Categoria, CategoriaAdmin)
