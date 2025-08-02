from django.shortcuts import render
#from .models import Noticia,Categoria
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy

# Create your views here.

#Esto es solo para probar que todo funcione correctamente
def prueba(request):
    return render(request,'index.html')