from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse,reverse_lazy
from django.views import generic
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .pagination import PostSetPagination
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.renderers import (
                                        HTMLFormRenderer, 
                                        JSONRenderer, 
                                        BrowsableAPIRenderer,
                                    )
import base64
from .image_renderer import JPEGRenderer, PNGRenderer

class post_list(APIView, PageNumberPagination):
    serializer_class = PostSerializer
    pagination_class = PostSetPagination

    def get(self, request, pk_a):
        """
        Get the list of posts on our website
        """
        author = Author.objects.get(id=pk_a)
        posts = Post.objects.filter(author=author)
        posts = self.paginate_queryset(posts, request) 
        serializer = PostSerializer(posts, many=True)
        return  self.get_paginated_response(serializer.data)

    def post(self, request, pk_a):
        post_id = uuid.uuid4
        
        try:
            author = Author.objects.get(pk=pk_a)
        except Author.DoesNotExist:
            error_msg = "Author id not found"
            return Response(error_msg, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(data=request.data, context={'author_id': pk_a})
        if serializer.is_valid():
            # using raw create because we need custom id
            # print("original",serializer.validated_data.get('categories'))
            # categories = ' '.join(serializer.validated_data.get('categories'))
            # print("categories", categories)
            #serializer.validated_data.pop('categories')
            serializer.validated_data.pop("author")
            post = Post.objects.create(**serializer.validated_data, author=author, id=post_id)
            post.update_fields_with_request(request)

            serializer = PostSerializer(post, many=False)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_comments(request, pk_a, pk):
    """
    Get the list of comments on our website
    """
    author = Author.objects.get(id=pk_a)
    post = Post.objects.get(author=author, id=pk)
    comments = Comment.objects.filter(author=author,post=post)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_likes(request, pk_a, pk):
    """
    Get the list of comments on our website
    """
    author = Author.objects.get(id=pk_a)
    post = Post.objects.get(author=author, id=pk)
    likes = Like.objects.filter(object=post.id)
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data)

class IndexView(generic.ListView):
    template_name = 'posts/index.html'
    context_object_name = 'latest_posts'

    def get_queryset(self):
        """Return the last five published posts."""
        return Post.objects.order_by('title')[:5]

class DetailView(generic.DetailView):
    model = Post
    context_object_name = 'postt'
    template_name = 'posts/detail.html'
    
class PostDeleteView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):

    model = Post
    template_name = 'posts/delete.html'
    context_object_name = 'post'
    success_url = '/admin/'
    
    def test_func(self):
        post = self.get_object()
        print(post.title)
        if self.request.user == post.author.user:
            return True
        return False

class ImageView(APIView):
    renderer_classes = [JPEGRenderer, PNGRenderer]

    def post(self):
        # DO THIS
        return

    def get(self, request, pk_a, pk):
        try:
            author = Author.objects.get(id=pk_a) 
            post = Post.objects.get(author=author, id=pk)
            # not image post
            if 'image' not in post.contentType:
                return Response(status=status.HTTP_404_NOT_FOUND)

            # not properly base64 encoded yet
            post_content = post.contentType.split(';')[0]
            # image = base64.b64decode(post.content.strip("b'").strip("'"))
            return Response(post.image, content_type=post_content, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        