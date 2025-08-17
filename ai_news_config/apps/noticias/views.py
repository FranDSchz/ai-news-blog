from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Post, Categoria, Video
from .forms import PostForm 

#DEUDA TECNICA: Implementar manejo de errores, que pasa si hay menos de 10 noticias publicadas?
def home(request):
    #CONSULTAS a la BD
    posts_recientes = Post.objects.filter(estado='publicado').order_by('-fecha_publicacion')[:25]
    categorias_whats_new = Categoria.objects.all()
    videos = Video.objects.order_by('-fecha_creacion')[:5]
    
    categorias_con_posts = []
    for cat in categorias_whats_new:
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
        'categorias_whats_new': categorias_whats_new,
        'posts_whats_new': posts_whats_new,
        'weekly2_news_posts': weekly2_news_posts,
        'recent_articles_posts': recent_articles_posts,
        'data': categorias_con_posts,
        'videos': videos
    }
    
    return render(request, 'noticias/home.html', context)

#LOS DECORADORES PROTEGEN LAS VISTAS PARA QUE SOLO PUEDAN USARLAS LOS COLABORADORES

def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    categorias = post.categoria.all()
    context = {'post':post, 'categorias':categorias}
    print(post)
    return render(request,'noticias/post_detail.html',context)

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
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'noticias/post_form.html', {'form': form, 'titulo': 'Editar Post'})


@login_required
@permission_required('noticias.delete_post', raise_exception=True)
def post_eliminar(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'El post ha sido eliminado.')
        return redirect('home')
    return render(request, 'noticias/post_confirmar_eliminar.html', {'post': post})
