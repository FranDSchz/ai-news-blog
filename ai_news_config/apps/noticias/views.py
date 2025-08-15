from django.shortcuts import render, get_object_or_404
from .models import Post
# Create your views here.

def home(request):
    posts = Post.objects.filter(estado='publicado').order_by('-fecha_publicacion')
    context = {'posts':posts}
    return render(request,'home.html',context)

def post_detail(request,id_post):
    post = get_object_or_404(Post,id=id_post)
    context = {'post':post}
    print(post)
    return render(request,'noticias/post_detail.html',context)