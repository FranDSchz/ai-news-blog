from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Categoria, Video, Comentario, Notificacion
from apps.usuarios.models import Usuario
from .forms import PostForm, ComentarioForm, ComentarioUpdateForm, CategoriaForm, VideoForm, PostFilterForm
from django.db.models import Count, Q
from django.http import Http404
from django.utils import timezone


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
        'posts_whats_new': posts_whats_new,
        'weekly2_news_posts': weekly2_news_posts,
        'recent_articles_posts': recent_articles_posts,
        'data': categorias_con_posts,
        'videos': videos
    }
    
    return render(request, 'noticias/home.html', context)

#LOS DECORADORES PROTEGEN LAS VISTAS PARA QUE SOLO PUEDAN USARLAS LOS COLABORADORES

def post_detail(request,pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404("El post que buscas no existe.")

    if post.estado == 'borrador':
        if not request.user.is_authenticated or (request.user != post.autor and not request.user.is_superuser):
            messages.error(request, "Este artículo aún no ha sido publicado.")
            return redirect('home')
    
    posts_recientes = Post.objects.filter(estado='publicado').exclude(pk=pk).order_by('-fecha_publicacion')[:5] #DEFINIR BIEN EL CRITERIO PARA MOSTRAR ESTOS POST.
    
    categorias_post = post.categoria.all()
    comentarios = Comentario.objects.filter(post=post).select_related('usuario__perfil')
    count_coment = comentarios.count()
    fecha_referencia = post.fecha_publicacion or timezone.now()
    prev_post = Post.objects.filter(
        estado='publicado',
        categoria__in=categorias_post, 
        fecha_publicacion__lt=fecha_referencia
    ).exclude(pk=post.pk).distinct().order_by('-fecha_publicacion', '-id').first()
    
    next_post = Post.objects.filter(
        estado='publicado',
        categoria__in=categorias_post,
        fecha_publicacion__gt=fecha_referencia
    ).exclude(pk=post.pk).distinct().order_by('fecha_publicacion', 'id').first()
    
    perfil_autor = post.autor.perfil
    
    
    
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
    cat_count = Categoria.objects.annotate(
        num_posts=Count('posts', filter=Q(posts__estado='publicado'))
    )

    context = {
        'post': post,
        'posts_recientes': posts_recientes,
        'categorias_post': categorias_post,
        'comentarios': comentarios,       
        'comentario_form': comentario_form,
        'count_coment':count_coment,
        'perfil_autor': perfil_autor,
        'next_post':next_post,
        'prev_post':prev_post,
        'cat_count':cat_count
    }            
    
    return render(request,'noticias/post_detail.html',context)

def buscar_posts(request):
    query = request.GET.get('q')
    posts = []
    if query:
        posts = Post.objects.filter(
            Q(titulo__icontains=query) | 
            Q(contenido__icontains=query)
        ).distinct()
    return render(request, 'noticias/resultados_busqueda.html', {'posts': posts, 'query': query})

def posts_por_categoria(request, categoria_id=None):
    # 1. Definimos el queryset base
    posts = Post.objects.filter(estado='publicado')
    categoria = None
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
        
    cat_count = Categoria.objects.annotate(
        num_posts=Count('posts', filter=Q(posts__estado='publicado'))
    )
    context = {
        'categoria': categoria,
        'posts': posts,
        'orden_actual': orden,
        'cat_count':cat_count
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
    }
    return render(request, 'noticias/explorar_noticias.html', context)

@login_required
def post_crear(request):
    if not (request.user.rol == Usuario.AUTOR or request.user.is_superuser):
        messages.error(request, 'No tienes permiso para crear un artículo.')
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save() 
            form.save_m2m() # Necesario para guardar las relaciones ManyToMany (categorías)

            # Mensaje de éxito dinámico
            if post.estado == 'publicado':
                messages.success(request, f'¡El artículo "{post.titulo}" ha sido publicado exitosamente!')
            else:
                messages.success(request, f'¡El artículo "{post.titulo}" ha sido guardado como borrador!')
            
            return redirect('noticias:mis_articulos')
    else:
        form = PostForm()
    
    # Si el formulario no es válido, se volverá a renderizar la plantilla
    # con los errores almacenados en el objeto 'form'.
    return render(request, 'noticias/post_forms.html', {'form': form, 'titulo': 'Crear Nuevo Artículo'})


@login_required
def post_editar(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 1. Comprobación de Rol Y Propiedad
    if not (request.user == post.autor or request.user.is_superuser):
        messages.error(request, 'No tienes permiso para editar este artículo.')
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '¡El artículo ha sido actualizado!')
            return redirect('noticias:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'noticias/post_forms.html', {'form': form, 'titulo': f'Editar: {post.titulo}'})


@login_required
def post_eliminar(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 1. Comprobación de Rol Y Propiedad
    if not (request.user == post.autor or request.user.is_superuser):
        messages.error(request, 'No tienes permiso para eliminar este artículo.')
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'El artículo ha sido eliminado.')
        return redirect('noticias:mis_articulos') # Redirige al panel del autor
    return render(request, 'noticias/post_confirmar_eliminar.html', {'post': post})

@login_required
def lista_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario_destino=request.user).order_by('-fecha_creacion')
    
    Notificacion.objects.filter(usuario_destino=request.user, leida=False).update(leida=True)
    
    return render(request, 'noticias/notificaciones.html', {'notificaciones': notificaciones})

@login_required
def mis_articulos(request):
    # Asegurarse de que solo los autores y admins puedan acceder
    if not (request.user.rol == Usuario.AUTOR or request.user.is_superuser):
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('home')

    # Obtenemos todos los posts del usuario logueado, ordenados por fecha
    posts = Post.objects.filter(autor=request.user).order_by('-fecha_creacion')
    
    context = {
        'posts': posts,
    }
    return render(request, 'noticias/mis_articulos.html', context)

@login_required
def comentario_editar(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)

    # Solo el autor del comentario puede editarlo
    if request.user != comentario.usuario:
        messages.error(request, 'No tienes permiso para editar este comentario.')
        return redirect('noticias:post_detail', pk=comentario.post.pk)

    if request.method == 'POST':
        form = ComentarioUpdateForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu comentario ha sido actualizado.')
            return redirect('noticias:post_detail', pk=comentario.post.pk)
    else:
        form = ComentarioUpdateForm(instance=comentario)

    # Renderizaremos un nuevo template para el formulario de edición
    return render(request, 'noticias/comentario_editar.html', {'form': form, 'comentario': comentario})


@login_required
def comentario_eliminar(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    post_pk = comentario.post.pk

    # Permisos: El autor del comentario, el autor del post o un admin pueden eliminar
    if not (request.user == comentario.usuario or request.user == comentario.post.autor or request.user.is_superuser):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('noticias:post_detail', pk=post_pk)

    if request.method == 'POST':
        # Personalizamos el mensaje de eliminación
        if request.user == comentario.usuario:
            comentario.texto = "[Comentario eliminado por el autor original]"
        else:
            comentario.texto = f"[Comentario eliminado por moderador: {request.user.username}]"
        
        comentario.eliminado = True
        comentario.eliminado_por = request.user # Guardamos quién lo eliminó
        comentario.save()
        messages.success(request, 'El comentario ha sido eliminado.')
    
    return redirect('noticias:post_detail', pk=post_pk)

@login_required
def gestionar_categorias(request):
    if not (request.user.rol == Usuario.AUTOR or request.user.is_superuser):
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('home')
    
    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, 'noticias/gestionar_categorias.html', {'categorias': categorias})

@login_required
def categoria_crear(request):
    if not (request.user.rol == Usuario.AUTOR or request.user.is_superuser):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('home')

    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Categoría creada exitosamente!')
            return redirect('noticias:gestionar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'noticias/generic_form.html', {'form': form, 'titulo': 'Crear Nueva Categoría'})

@login_required
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if not (request.user.rol == Usuario.AUTOR or request.user.is_superuser):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('home')

    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Categoría actualizada exitosamente!')
            return redirect('noticias:gestionar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'noticias/generic_form.html', {'form': form, 'titulo': f'Editar: {categoria.nombre}'})

@login_required
def categoria_eliminar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if not (request.user.rol == Usuario.AUTOR or request.user.is_superuser):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('home')

    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'La categoría ha sido eliminada.')
        return redirect('noticias:gestionar_categorias')
    return render(request, 'noticias/generic_delete_confirm.html', {'objeto': categoria, 'titulo': 'Confirmar Eliminación de Categoría'})

@login_required
def gestionar_videos(request):
    if not (request.user.rol == Usuario.AUTOR or request.user.is_superuser):
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('home')
    
    videos = Video.objects.all().order_by('-fecha_creacion')
    return render(request, 'noticias/gestionar_videos.html', {'videos': videos})

@login_required
def video_crear(request):
    if not (request.user.rol == Usuario.AUTOR or request.user.is_superuser):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('home')

    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Video añadido exitosamente!')
            return redirect('noticias:gestionar_videos')
    else:
        form = VideoForm()
    return render(request, 'noticias/generic_form.html', {'form': form, 'titulo': 'Añadir Nuevo Video'})

@login_required
def video_editar(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if not (request.user.rol == Usuario.AUTOR or request.user.is_superuser):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('home')

    if request.method == 'POST':
        form = VideoForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Video actualizado exitosamente!')
            return redirect('noticias:gestionar_videos')
    else:
        form = VideoForm(instance=video)
    return render(request, 'noticias/generic_form.html', {'form': form, 'titulo': f'Editar: {video.titulo}'})

@login_required
def video_eliminar(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if not (request.user.rol == Usuario.AUTOR or request.user.is_superuser):
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('home')

    if request.method == 'POST':
        video.delete()
        messages.success(request, 'El video ha sido eliminado.')
        return redirect('noticias:gestionar_videos')
    return render(request, 'noticias/generic_delete_confirm.html', {'objeto': video, 'titulo': 'Confirmar Eliminación de Video'})