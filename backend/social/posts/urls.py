from django.urls import path
from . import views
from .views import *


app_name = 'posts'
urlpatterns = [
  path('authors/<str:pk_a>/posts/', views.post_list.as_view(), name = "posts"),
  path('authors/<str:pk_a>/posts/<str:pk>/', views.post_detail.as_view(), name='detail'),
  # path('authors/<str:pk_a>/posts/<str:pk>/comments/', views.get_comments, name='get_comments'),
  path('authors/<str:pk_a>/posts/<str:pk>/comments/', views.CommentView.as_view(), name='comments'),
  # path('authors/<str:pk_a>/posts/<str:pk>/comments/', CommentCreateView.as_view(), name='comments_create'),
  path('authors/<str:pk_a>/posts/<str:pk>/likes/', views.get_likes, name='get_likes'),
  path('authors/<str:pk_a>/inbox/', views.LikeView.as_view(), name = "likes"),

]
