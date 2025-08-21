"""
URL configuration for ai_news_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.noticias.views import home
from django.conf import settings
from django.conf.urls.static import static
from apps.usuarios.views import contacto
from django.views.generic import TemplateView

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('noticias/',include('apps.noticias.urls')),
    path('usuarios/', include('apps.usuarios.urls', 'usuarios')),
    path('contacto/', contacto,name= 'contacto'),
    path('nosotros/', TemplateView.as_view(template_name='nosotros.html'), name='nosotros'),
]

if settings.DEBUG:  # Solo en desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)