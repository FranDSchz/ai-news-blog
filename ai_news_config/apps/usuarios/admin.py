from django.contrib import admin
from .models import Usuario


# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active') 
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    ordering = ('-date_joined',)
    readonly_fields = ('last_login', 'date_joined')
    

admin.site.register(Usuario,UsuarioAdmin)