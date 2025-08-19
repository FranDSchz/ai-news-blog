#Probando que funcione todo
from django.shortcuts import render

def nosotros(request):
    return render(request,'nosotros.html')

def contacto(request):
    return render(request,'contacto.html')