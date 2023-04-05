from django.urls import path
from . import views
from .views import *


app_name = 'posts'
urlpatterns = [
  path('public/', views.PublicPostsView.as_view(), name = "explore"),
]
