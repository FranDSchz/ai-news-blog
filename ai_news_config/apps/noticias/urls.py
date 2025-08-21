from django.urls import path
from .views import home, posts_por_categoria, lista_notificaciones, post_detail,post_crear,post_editar,post_eliminar, lista_categorias,posts_por_categoria, explorar_noticias, buscar_posts
app_name = 'noticias'
urlpatterns = [
    path('', home, name='home'),
    path('categorias/', lista_categorias, name='lista_categorias'),
    path('categoria/<int:categoria_id>', posts_por_categoria, name='posts_por_categoria'),
    path('detalle/<int:pk>/', post_detail, name='post_detail'),
    path('post/crear/', post_crear, name='post_crear'),
    path('post/<int:pk>/editar/', post_editar, name='post_editar'),
    path('post/<int:pk>/eliminar/', post_eliminar, name='post_eliminar'),
    path('explorar/', explorar_noticias, name='explorar_noticias'),
    path('buscar/', buscar_posts, name='buscar_posts'),
    path('categorias/filtro/<int:categoria_id>/', posts_por_categoria, name='categorias_filtro'),
    path('notificaciones/', lista_notificaciones, name='lista_notificaciones')
]
