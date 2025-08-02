from django.urls import path
from .views import prueba
#probando que todo ande
urlpatterns = [
    path('',prueba,name="prueba"),
]