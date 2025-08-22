from django.urls import path
#from .views import comentario_editar,comentario_eliminar,home, posts_por_categoria, lista_notificaciones, post_detail,post_crear,post_editar,post_eliminar, lista_categorias,posts_por_categoria, explorar_noticias, buscar_posts,mis_articulos
from . import views
app_name = 'noticias'
urlpatterns = [
    path('', views.home, name='home'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categoria/<int:categoria_id>', views.posts_por_categoria, name='posts_por_categoria'),
    path('detalle/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/crear/', views.post_crear, name='post_crear'),
    path('post/<int:pk>/editar/', views.post_editar, name='post_editar'),
    path('post/<int:pk>/eliminar/', views.post_eliminar, name='post_eliminar'),
    path('explorar/', views.explorar_noticias, name='explorar_noticias'),
    path('buscar/', views.buscar_posts, name='buscar_posts'),
    path('notificaciones/', views.lista_notificaciones, name='lista_notificaciones'),
    path('mis-articulos/', views.mis_articulos, name='mis_articulos'),
    path('comentario/<int:pk>/editar/', views.comentario_editar, name='comentario_editar'),
    path('comentario/<int:pk>/eliminar/', views.comentario_eliminar, name='comentario_eliminar'),
    path('gestionar/categorias/', views.gestionar_categorias, name='gestionar_categorias'),
    path('categoria/crear/', views.categoria_crear, name='categoria_crear'),
    path('categoria/<int:pk>/editar/', views.categoria_editar, name='categoria_editar'),
    path('categoria/<int:pk>/eliminar/', views.categoria_eliminar, name='categoria_eliminar'),
    path('gestionar/videos/', views.gestionar_videos, name='gestionar_videos'),
    path('video/crear/', views.video_crear, name='video_crear'),
    path('video/<int:pk>/editar/', views.video_editar, name='video_editar'),
    path('video/<int:pk>/eliminar/', views.video_eliminar, name='video_eliminar'),
]
