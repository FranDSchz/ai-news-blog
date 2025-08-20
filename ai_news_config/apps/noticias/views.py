from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Post, Categoria, Video, Comentario
from .forms import PostForm, ComentarioForm
from django.db.models import Count, Q
from .forms import PostFilterForm

#DEUDA TECNICA: Implementar manejo de errores, que pasa si hay menos de 10 noticias publicadas?
def home(request):
    #CONSULTAS a la BD
    posts_recientes = Post.objects.filter(estado='publicado').order_by('-fecha_publicacion')[:25]
    categorias = Categoria.objects.all()
    videos = Video.objects.order_by('-fecha_creacion')[:5]
    
    categorias_con_posts = []
    for cat in categorias:
        aux = Post.objects.filter(categoria=cat).order_by('-fecha_publicacion')[:4]
        categorias_con_posts.append({
            'cat': cat,
            'posts': aux
        })
        
    
    #CUANDO QUIERA APLICAR OTRO CRITERIO VOY A TENER QUE CAMBIAR COMO DEFINO ESTAS VARIABLES
    posts_whats_new = posts_recientes[:4]
    trending_title_posts = posts_recientes[:5]
    trending_top_post = posts_recientes[0] if len(posts_recientes) > 0 else None
    trending_bottom_posts =  posts_recientes[1:4]
    right_content_posts = posts_recientes[4:9]
    weekly_news_posts = posts_recientes[10:14]
    weekly2_news_posts= posts_recientes[14:19]
    recent_articles_posts = posts_recientes[19:23]
    context = {
        'trending_title_posts': trending_title_posts,
        'trending_top_post': trending_top_post,
        'trending_bottom_posts': trending_bottom_posts,
        'right_content_posts': right_content_posts,
        'weekly_news_posts': weekly_news_posts,
        'categorias': categorias,
        'posts_whats_new': posts_whats_new,
        'weekly2_news_posts': weekly2_news_posts,
        'recent_articles_posts': recent_articles_posts,
        'data': categorias_con_posts,
        'videos': videos
    }
    
    return render(request, 'noticias/home.html', context)

#LOS DECORADORES PROTEGEN LAS VISTAS PARA QUE SOLO PUEDAN USARLAS LOS COLABORADORES

def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk, estado = 'publicado')
    
    posts_recientes = Post.objects.filter(estado='publicado').exclude(pk=pk).order_by('-fecha_publicacion')[:5] #DEFINIR BIEN EL CRITERIO PARA MOSTRAR ESTOS POST.
    
    categorias_post = post.categoria.all()
    comentarios = Comentario.objects.filter(post=post).select_related('usuario__perfil')
    count_coment = comentarios.count()
    
    prev_post = Post.objects.filter(
        estado='publicado',
        categoria__in=categorias_post, 
        fecha_publicacion__lt=post.fecha_publicacion
    ).exclude(pk=post.pk).distinct().order_by('-fecha_publicacion', '-id').first()
    
    next_post = Post.objects.filter(
        estado='publicado',
        categoria__in=categorias_post,
        fecha_publicacion__gt=post.fecha_publicacion
    ).exclude(pk=post.pk).distinct().order_by('fecha_publicacion', 'id').first()
    
    perfil_autor = post.autor.perfil
    
    categorias = Categoria.objects.all()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para poder comentar.')
            return redirect('apps.usuarios:login')
        comentario_form = ComentarioForm(request.POST)
        if comentario_form.is_valid():
            # Creamos el objeto Comentario pero no lo guardamos aún en la base de datos.
            nuevo_comentario = comentario_form.save(commit=False)
            # Le asignamos manualmente el post actual.
            nuevo_comentario.post = post
            # Le asignamos manualmente el usuario que está logueado.
            nuevo_comentario.usuario = request.user
            # Ahora sí, guardamos el comentario completo en la base de datos.
            nuevo_comentario.save()
            messages.success(request, '¡Tu comentario se ha publicado con éxito!')
            # Redirigimos al usuario a la misma página para que vea su nuevo comentario y
            # evitar que se reenvíe el formulario si recarga la página.
            return redirect('noticias:post_detail', pk=post.pk)
    else:
        comentario_form = ComentarioForm()
        
    context = {
        'post': post,
        'posts_recientes': posts_recientes,
        'categorias_post': categorias_post,
        'categorias':categorias,
        'comentarios': comentarios,       
        'comentario_form': comentario_form,
        'count_coment':count_coment,
        'perfil_autor': perfil_autor,
        'next_post':next_post,
        'prev_post':prev_post
    }            
    
    return render(request,'noticias/post_detail.html',context)

def posts_por_categoria(request, categoria_id=None):
    # 1. Definimos el queryset base
    posts = Post.objects.filter(estado='publicado')
    categoria = None
    categorias_base = Categoria.objects.all()
    # 2. Si se proporciona un categoria_id, filtramos por esa categoría
    if categoria_id:
        categoria = get_object_or_404(Categoria, id=categoria_id)
        posts = posts.filter(categoria=categoria)

    # 3. Lógica de ordenamiento (sin cambios)
    orden = request.GET.get('ordenar', 'fecha_desc')
    if orden == 'fecha_asc':
        posts = posts.order_by('fecha_publicacion')
    elif orden == 'titulo_asc':
        posts = posts.order_by('titulo')
    elif orden == 'titulo_desc':
        posts = posts.order_by('-titulo')
    else:
        posts = posts.order_by('-fecha_publicacion')

    context = {
        'categoria': categoria,
        'posts': posts,
        'orden_actual': orden,
        'categorias':categorias_base
    }
    return render(request, 'noticias/categoria_posts.html', context)



def lista_categorias(request):
    # La condición se aplica DENTRO del Count usando el parámetro "filter"
    categorias = Categoria.objects.annotate(
        num_posts=Count('posts', filter=Q(posts__estado='publicado'))
    )

    context = {
        'categorias': categorias
    }
    return render(request, 'noticias/lista_categorias.html', context)

def explorar_noticias(request):
    # Empezamos con el QuerySet base que incluye todos los posts publicados
    queryset = Post.objects.filter(estado='publicado')
    
    # Creamos una instancia de nuestro formulario, pasándole los datos que vienen por GET
    # request.GET contendrá un diccionario como {'categoria': '1', 'ordenar': 'titulo_asc'}
    form = PostFilterForm(request.GET)
    categorias = Categoria.objects.all()
    # Django validará que los datos recibidos son coherentes con el formulario
    if form.is_valid():
        cleaned_data = form.cleaned_data

        # Filtro por categoría (si se seleccionó una)
        if cleaned_data['categoria']:
            queryset = queryset.filter(categoria=cleaned_data['categoria'])

        # Ordenamiento
        orden = cleaned_data.get('ordenar') or 'fecha_desc' # Usamos el valor del form o el default
        if orden == 'fecha_asc':
            queryset = queryset.order_by('fecha_publicacion')
        elif orden == 'titulo_asc':
            queryset = queryset.order_by('titulo')
        elif orden == 'titulo_desc':
            queryset = queryset.order_by('-titulo')
        else: # 'fecha_desc'
            queryset = queryset.order_by('-fecha_publicacion')

    context = {
        'posts': queryset,
        'filter_form': form, # Pasamos el formulario a la plantilla
        'categorias':categorias
    }
    return render(request, 'noticias/explorar_noticias.html', context)

@login_required
@permission_required('noticias.add_post', raise_exception=True)
def post_crear(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            messages.success(request, '¡El post ha sido creado exitosamente!')
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'noticias/post_forms.html', {'form': form, 'titulo': 'Crear Nuevo Post'})


@login_required
@permission_required('noticias.change_post', raise_exception=True)
def post_editar(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '¡El post ha sido actualizado!')
            return redirect('noticias:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'noticias/post_forms.html', {'form': form, 'titulo': 'Editar Post'})


@login_required
@permission_required('noticias.delete_post', raise_exception=True)
def post_eliminar(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'El post ha sido eliminado.')
        return redirect('home')
    return render(request, 'noticias/post_confirmar_eliminar.html', {'post': post})
