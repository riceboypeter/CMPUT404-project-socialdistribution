import uuid
from django.urls import reverse
from rest_framework import serializers, exceptions
from .models import *
from rest_framework import status
from rest_framework.response import Response
import client
from Remote.Authors import getNodeAuthor_App2

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="author",source="get_api_type",read_only=True)
    id = serializers.URLField(source="get_public_id",read_only=True)
    url = serializers.URLField(source="get_absolute_url",read_only=True)
    displayName = serializers.CharField(default = 'x')
    
    @staticmethod
    def _update(validated_data):
        print("AUTHOR ID", validated_data["id"])
        id = validated_data["id"].split("/")[-1]
        author = Author.objects.get(id=id)
        return author
        #return super().update(author,validated_data)
    
    @staticmethod
    def _upcreate(validated_data):
        print("in the other upcreate function")
        return Author(**validated_data)
    
    @staticmethod
    def extract_and_upcreate_author(validated_data, author_id = None):
        print("in extract and upcreate")
        if author_id is not None:
            try:
                return Author.objects.get(id=author_id)
            except Author.DoesNotExist:
                return Response("Author does not exist here!", status=status.HTTP_404_NOT_FOUND)
        updated_author = None
        try:
            updated_author = AuthorSerializer._update(validated_data)
        except Author.DoesNotExist:
            updated_author = AuthorSerializer._upcreate(validated_data)
            print("updated author saved")
        if not updated_author:
            print("no author", updated_author)
            return Response("Author does not exist here!", status=status.HTTP_404_NOT_FOUND)
        else:
            return updated_author.save()            
    
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








