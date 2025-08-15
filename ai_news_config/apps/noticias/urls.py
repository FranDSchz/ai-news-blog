from django.urls import path
from .views import home, post_detail

urlpatterns = [
    path('<int:id_post>/', post_detail, name="post_detail"),
]
