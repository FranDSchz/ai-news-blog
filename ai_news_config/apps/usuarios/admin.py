from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Perfil,MensajeContacto


class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'
    fk_name = 'usuario'

class CustomUserAdmin(UserAdmin):
    inlines = (PerfilInline, )
    list_display = ('username', 'email', 'rol', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'rol', 'date_joined')
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
        
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('asunto', 'nombre', 'email', 'fecha_enviado', 'leido')
    list_filter = ('leido', 'fecha_enviado')
    search_fields = ('nombre', 'email', 'asunto', 'mensaje')
    readonly_fields = ('nombre', 'email', 'asunto', 'mensaje', 'fecha_enviado')



admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(MensajeContacto,MensajeContactoAdmin)
