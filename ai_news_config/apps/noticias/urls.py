from django.urls import path
from .views import home, post_detail

urlpatterns = [
    path('<int:pk>/', post_detail, name="post_detail"),
]
