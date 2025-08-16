from django.shortcuts import render, get_object_or_404
from .models import Post

#DEUDA TECNICA: Implementar manejo de errores, que pasa si hay menos de 10 noticias publicadas?
def home(request):
    # 1. Hacemos una consulta para obtener los 10 posts más recientes.
    #    Pedimos 10 para cubrir todas las secciones (1 top + 3 bottom + 6 right).
    posts_recientes = Post.objects.filter(estado='publicado').order_by('-fecha_publicacion')[:10]
    
    #CUANDO QUIERA APLICAR OTRO CRITERIO VOY A TENER QUE CAMBIAR COMO DEFINO ESTAS VARIABLES
    trending_title_posts = posts_recientes[:5]
    trending_top_post = posts_recientes[0] if len(posts_recientes) > 0 else None
    trending_bottom_posts =  posts_recientes[1:4]
    right_content_posts = posts_recientes[4:9]
    # 2. Preparamos el contexto con nombres claros para cada sección.
    #    Usamos slicing para dividir la lista de posts.
    context = {
        # Para el "Trending Title", podemos reusar los 5 primeros.
        'trending_title_posts': trending_title_posts ,
        
        # El post principal es el primero de la lista (índice 0).
        # Agregamos una comprobación para evitar errores si no hay posts.
        'trending_top_post': trending_top_post,
        
        # Los 3 siguientes son para la sección de abajo (del índice 1 al 4, sin incluir el 4).
        'trending_bottom_posts': trending_bottom_posts,

        # Los 6 restantes son para la barra lateral derecha (del índice 4 al 10). 
        'right_content_posts': right_content_posts
    }
    
    return render(request, 'noticias/home.html', context)

def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    categorias = post.categoria.all()
    context = {'post':post, 'categorias':categorias}
    print(post)
    return render(request,'noticias/post_detail.html',context)