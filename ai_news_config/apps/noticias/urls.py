from django.urls import path
from .views import home, post_detail
from . import views
app_name = 'noticias'
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/', post_detail, name="post_detail"),
    path('post/crear/', views.post_crear, name='post_crear'),
    path('post/<int:pk>/editar/', views.post_editar, name='post_editar'),
    path('post/<int:pk>/eliminar/', views.post_eliminar, name='post_eliminar'),
]
