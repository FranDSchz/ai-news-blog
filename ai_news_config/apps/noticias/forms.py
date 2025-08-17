# ai_news_config/apps/noticias/forms.py

from django import forms
from .models import Post

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