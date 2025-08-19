# ai_news_config/apps/noticias/forms.py

from django import forms
from .models import Post, Categoria, Comentario

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'imagen', 'categoria', 'estado']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe el título'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'categoria': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        # Usamos 'texto' para que coincida con tu modelo
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe tu comentario aquí...',
                'rows': 5, # Puedes ajustar el número de filas
                'id': 'comment' # Usamos el id que probablemente espera el CSS de la plantilla
            }),
        }
        labels = {
            'texto': '', # Dejamos la etiqueta vacía para que no aparezca "Texto:"
        }