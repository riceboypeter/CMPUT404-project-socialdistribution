from django.db import models
from django.urls import reverse
from author.models import Author, Inbox
from django.contrib.contenttypes.fields import GenericRelation
import uuid
from django.conf import settings


# Create your models here.

PUBLIC = 'PUBLIC'
PRIVATE = 'PRIVATE'
FRIENDS = 'FRIENDS'

# 
visbility_choices = [
    (PUBLIC, 'Public'),
    (PRIVATE, 'Private'),
    (FRIENDS, 'Friends')
]

MARKDOWN = 'text/markdown'
PLAIN = 'text/plain'
IMAGE_PNG = 'image/png' 
IMAGE_JPEG = 'image/jpeg'

content_types = [
    (MARKDOWN, 'markdown'),
    (PLAIN, 'plain'),
    (IMAGE_PNG, 'image/png;base64'),
    (IMAGE_JPEG, 'image/jpeg;base64'),
]

class Post(models.Model):
    id = models.CharField(primary_key=True, editable=False, default= uuid.uuid4, max_length=255)
    url = models.URLField(editable=False, max_length=255)  # url of post
    author = models.ForeignKey(Author, related_name="posts", on_delete=models.CASCADE)  # author of post
    categories = models.CharField(max_length=255, default="", blank=True)
    title = models.CharField(max_length=150)  # title of post
    source = models.URLField(editable=False,max_length=500)  # source of post IE the url of where the post is located
    origin = models.URLField(editable=False,max_length=500)  # origin of post IE the url of where the originl post is located if shared.
    description = models.CharField(blank=True, default="", max_length=200)  # brief description of post
    contentType = models.CharField(choices=content_types, default=PLAIN, max_length=20)  # type of content
    content = models.TextField(blank=False, default="")  # content of post
    visibility = models.CharField(choices=visbility_choices, default=PUBLIC, max_length=20)  # visibility status of post
    inbox = GenericRelation(Inbox, related_query_name='post')  # inbox in which post is in
    published = models.DateTimeField(auto_now_add=True)  # date published
    count = models.PositiveIntegerField(default=0, blank=True)
    commentsSrc = models.CharField(max_length=255, default="", blank=True)
    is_github = models.BooleanField(default=False)
    unlisted = models.BooleanField(default=False)
    
    image = models.ImageField(null=True,blank=True, default="")  # reference to an image in the DB

    # make it pretty
    def __str__(self):
        return self.title + " (" + str(self.id) + ")"
    
    def get_source(self):
        #set post source (URL to source)
        if not self.source:
            url = reverse('authors:post_detail', args=[str(self.author.id), str(self.id)])
            source = settings.APP_NAME + url
            self.source = source[:-1] if source.endswith('/') else source 
            self.save()
            return self.source
        return self.source
        
    def get_origin(self):
        #set post origin (URL to origin)
        if not self.origin:
            self.origin = self.get_source()
            self.save()
        return self.origin
    
    # get visbility status
    def get_visilibility(self):
        return self.Visibility(self.visibility).label
    
    # get content type
    def get_content_type(self):
        return self.ContentType(self.content_type).label

    # get public id of post
    def get_public_id(self):
        self.get_source()
        return (self.source) or str(self.id)
    
    # get comments url
    def get_comments_source(self):
        return self.source + '/comments/'
        
    def get_likes_count(self):
        return 0
    
    def update_fields_with_request(self, request=None):
        if not request:
            return
        self.url = request.build_absolute_uri(self.get_absolute_url())
        self.save()

    def get_absolute_url(self):
        if settings.HOST_NAME in self.source:
            url = reverse('authors:post_detail', args=[str(self.author.id), str(self.id)])
            url = settings.APP_NAME + url
            self.url = url[:-1] if url.endswith('/') else url 
            self.save()
            return self.url
        self.url = self.source
        self.url = self.url[:-1] if self.url.endswith('/') else self.url 
        self.save()
        return self.url
    
    @staticmethod
    def get_api_type():
        return 'post'
    
    class Meta:
        ordering = ['-published']
        
class Comment(models.Model):
    id = models.CharField(primary_key=True, editable=False, default= uuid.uuid4, max_length=255)  # ID of comment
    url = models.URLField(editable=False, max_length=500)  # URL of comment
    author = models.ForeignKey(Author, related_name = 'comments', on_delete=models.CASCADE)  # author of comment
    post = models.URLField(max_length=500) # post of the commenT
    comment = models.TextField()  # the comment
    published = models.DateTimeField(auto_now_add=True)  # date published
    contentType = models.CharField(choices=content_types, default=PLAIN, max_length=20)  # type of content
    inbox = GenericRelation(Inbox, related_query_name='comment')  # inbox in which post is in
    

    # get public id of comment
    def get_public_id(self):
        self.get_absolute_url()
        return (self.url) or str(self.id)
    
    def get_object(self):
        return self.post[-1] if self.post.endswith('/') else self.post 
    
    def get_absolute_url(self):
        if not self.id:
            self.post = self.post[:-1] if self.post.endswith('/') else self.post
            print(self.post)
            post = Post.objects.get(id=str(self.post.split("/")[-1]))
            url = reverse('authors:comment_detail', args=[post.id, str(self.post.split("/")[-1]), str(self.id)])
            print("Comment recieved")
            self.url = settings.APP_NAME + url
            self.save()
            return self.url
        else: 
            self.url = self.post + '/comments/' + self.id
            self.save()
            return self.url
    
    @staticmethod
    def get_api_type():
        return 'comment'
    
    class Meta:
        ordering = ['-published']

    def __str__(self):
        return 'Comment by {}'.format(self.author)
    
class Like(models.Model):
    id = models.CharField(primary_key=True, editable=False, default= uuid.uuid4, max_length=255)  # ID of like
    summary = models.CharField (max_length=100, default='')
    author = models.ForeignKey(Author, related_name = 'likes', on_delete=models.CASCADE)  # author of like
    object = models.URLField(max_length=500)  # URL of liked object
    inbox = GenericRelation(Inbox, related_query_name='like')  # inbox in which like is in

    def get_object(self):
        return self.object if self.object.endswith('/') else self.object + '/' 

    def get_summary(self):    
        return self.author.displayName + " Likes your " + str(self.object).split('/')[-2][:-1]

    @staticmethod
    def get_api_type():
        return 'Like'
    
    def __str__(self):
        return 'Liked by {}'.format(self.author)    