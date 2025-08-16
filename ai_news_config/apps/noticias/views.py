from django.shortcuts import render, get_object_or_404
from .models import Post
# Create your views here.

def home(request):
    posts = Post.objects.filter(estado='publicado').order_by('-fecha_publicacion')
    context = {'posts':posts}
    return render(request,'noticias/home.html',context)

def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    context = {'post':post}
    print(post)
    return render(request,'noticias/post_detail.html',context)