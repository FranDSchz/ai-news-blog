from django.urls import path
from .views import home, post_detail,post_crear,post_editar,post_eliminar, categorias,categorias_filtro
app_name = 'noticias'
urlpatterns = [
    path('', home, name='home'),
    path('<int:pk>/', post_detail, name='post_detail'),
    path('post/crear/', post_crear, name='post_crear'),
    path('post/<int:pk>/editar/', post_editar, name='post_editar'),
    path('post/<int:pk>/eliminar/', post_eliminar, name='post_eliminar'),
    path('categorias/', categorias, name='categorias'),
    path('categorias/<int:pk>', categorias_filtro, name='categorias_filtro'),
]
