import uuid
from django.urls import reverse
from rest_framework import serializers, exceptions
from .models import *
from rest_framework import status
from rest_framework.response import Response
import client
from Remote.Authors import getNodeAuthor_App2
from Remote.Authors import *


class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="author",source="get_api_type",read_only=True)
    id = serializers.URLField(source="get_public_id",read_only=True)
    url = serializers.URLField(source="get_absolute_url",read_only=True)
    displayName = serializers.CharField(default = '')
    
    # update author with provided instance
    def update(self, instance, validated_data):
        print(validated_data)
        print(instance)
        print("in update",type(validated_data))
        instance.url = validated_data.get('url', instance.url)
        instance.displayName = validated_data.get('displayName', instance.displayName)
        instance.github = validated_data.get('github', instance.github)
        instance.profileImage = validated_data.get('profileImage', instance.profileImage)
        return instance

    @staticmethod
    def _update(validated_data): 
        author = Author.objects.get(id=validated_data["id"])
        author_data = AuthorSerializer(author).update(instance=author,validated_data=validated_data)
        return author_data
    
    @staticmethod
    def _upcreate(validated_data):
        print("in the other upcreate function")
        print(validated_data)
        return Author(**validated_data)
    
    # 1. Return the author if it is hosted by our server
    # 2. Update author if author is hosted by another server and exists locally
    # 3. Create author if author is hosted by another server and does not exist locally
    @staticmethod
    def extract_and_upcreate_author(validated_data, author_id = None):
        print("in extract and upcreate", validated_data)
        if author_id is not None:
            try:
                return Author.objects.get(id=author_id)
            except Author.DoesNotExist:
                return Response("Author does not exist here!", status=status.HTTP_404_NOT_FOUND)
        updated_author = None
        if validated_data: 
            validated_data = clean_author(validated_data)
        try:
            updated_author = AuthorSerializer._update(validated_data)
            print("author is updated!")
        except Author.DoesNotExist:
            updated_author = AuthorSerializer._upcreate(validated_data)
            print("updated author saved")
        if not updated_author:
            print("no author", updated_author)
            return Response("Author does not exist here!", status=status.HTTP_404_NOT_FOUND)
        else:
            print("saved!")
            updated_author.save() 
            return updated_author     
    
    def to_representation(self, instance):
        id = instance.get_public_id()
        return {
            **super().to_representation(instance),
            'id': id
        }
        
    class Meta:
        model = Author
        fields = [
            'type', 
            'id', 
            'url',
            'host',
            'displayName',
            'github',
            'profileImage',
        ]

class FollowRequestSerializer(serializers.ModelSerializer):
    #to_user = serializers.CharField(default = 'x')
    type = serializers.CharField(default="Follow",source="get_api_type",read_only=True)
    summary = serializers.CharField(source="get_summary", read_only=True)
    actor = AuthorSerializer(required=False)
    object = AuthorSerializer(required=False)
    
    def create(self,validated_data):
        print("in follow req create")
        actor = validated_data["actor"]
        object = validated_data["object"]
        if actor in object.friends.all():
            print("already friends")
            return "already friends"
        if FollowRequest.objects.filter(actor=actor,object=object).exists():
            print("already sent")
            return "already sent"
        if actor==object:
            return "same"
        else:
            return FollowRequest.objects.create(actor=actor,object=object)
    
    # https://www.django-rest-framework.org/api-guide/serializers/
    def to_internal_value(self, data):
        print("to_internal_value")
        actor = AuthorSerializer.extract_and_upcreate_author(self.context["actor_"])
        object = Author.objects.get(id=self.context["object_id"])

        # Perform the data validation.
        if not actor:
            raise serializers.ValidationError({
                'actor': 'This field is required.'
            })
        if not object:
            raise serializers.ValidationError({
                'object': 'This field is required.'
            })
        
        return {
            'object': object,
            'actor': actor
        }
        
    class Meta:
        model = FollowRequest
        fields = ['type','summary','actor', 'object']
        
class InboxSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="inbox",source="get_api_type",read_only=True)

    def to_representation(self, instance):
        serializer = self.context["serializer"]
        rep = super().to_representation(instance)
        rep['content_object'] = serializer(instance)
        return rep

    class Meta:
        model = Inbox
        fields = ['type', 'author', 'content_type', 'object_id' ,'content_object']








