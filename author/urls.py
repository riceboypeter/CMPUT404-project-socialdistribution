from django.urls import path
from . import views
from .views import *
import posts.views as pview

app_name = 'authors'
urlpatterns = [
  path('', views.AuthorsListView.as_view(), name='get_authors'),
  path('<str:pk_a>/', views.AuthorView.as_view(), name='detail'),
  path('<str:pk_a>/github/', views.GitHubView.as_view(), name='github'),
  path('<str:pk_a>/inbox/', views.Inbox_list.as_view(), name='inbox'),
  path('<str:pk_a>/followers/', views.FollowersView.as_view(), name="get_followers"),
  path('<str:pk_a>/followers/<str:pk>/', views.FollowersView.as_view(), name="follow"),
  path('<str:pk_a>/sendreq/', views.FriendRequestView.as_view(), name='send_req'),
  path('<str:pk_a>/viewreq/', views.ViewRequests.as_view(), name='get_Requests'),
  path('<str:pk_a>/liked/', pview.LikedView.as_view(), name='get_liked'),
  path('displayName/<str:displayName>/', views.getAuthor),
  path('registerNode', views.registerNode.as_view(), name='register_node'),
  # For posts:
  path('<str:pk_a>/posts/', pview.PostListView.as_view(), name = "posts"),
  path('<str:pk_a>/posts/<str:pk>/', pview.post_detail.as_view(), name='post_detail'),
  path('<str:pk_a>/posts/<str:pk>/comments/', pview.CommentView.as_view(), name='comments'),
  path('<str:pk_a>/posts/<str:pk>/comments/<str:pk_m>/', pview.CommentDetailView.as_view(), name='comment_detail'),
  path('<str:pk_a>/posts/<str:pk>/likes/', pview.PostLikesView.as_view(), name='get_likes'),
  path('<str:pk_a>/posts/<str:pk>/comments/<str:pk_m>/likes/', pview.CommentLikesView.as_view(), name='get_comment_likes'),
  path('<str:pk_a>/posts/<str:pk>/image/', pview.ImageView.as_view()),
  path('<str:origin_author>/posts/<str:post_id>/share/<str:author>/', pview.ShareView.as_view(), name='share'),
]
