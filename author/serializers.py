import uuid
from django.urls import reverse
from rest_framework import serializers, exceptions
from .models import *
from django.http import HttpResponse
import client
from Remote.Authors import getNodeAuthor_App2

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="author",source="get_api_type",read_only=True)
    id = serializers.URLField(source="get_public_id",read_only=True)
    url = serializers.URLField(source="get_absolute_url",read_only=True)
    displayName = serializers.CharField(default = 'x')
    
    @staticmethod
    def _upcreate(validated_data):
        author = Author.objects.create(**validated_data)   
        return author
    @staticmethod
    def extract_and_upcreate_author(author_id=None):
        print("Author id is" + " " + author_id)
        #validated_author_data = validated_data.pop('author') if validated_data.get('author') else None
        updated_author= None
        try:
            updated_author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
           # updated_author = AuthorSerializer._upcreate(validated_data)
             #try other servers
             author, status = client.getNodeAuthor_Yoshi(author_id)
             if status != 200:
                author, status = client.getNodeAuthor_social_distro(author_id)
                if status == 200:
                    author = Author.objects.create(author)
             else: 
                updated_author = AuthorSerializer._upcreate()
                if status!= 200:
                    updated_author, status = getNodeAuthor_App2(author_id)
        #try to get authors from other servers
        if not updated_author:
            print("hello")
            raise exceptions.ValidationError("Author does not exist")
        else:
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
        if actor in object.friends.all():
            return "already friends"
        if FollowRequest.objects.get(actor=actor,object=object).exists():
            return "already sent"
        actor = validated_data["actor"]
        object = validated_data["object"]
        if actor==object:
            return "same"
        else:
            return FollowRequest.objects.create(actor=actor,object=object)

    # https://www.django-rest-framework.org/api-guide/serializers/
    def to_internal_value(self, data):
        actor = AuthorSerializer.extract_and_upcreate_author(author_id=self.context["actor_id"])
        object = AuthorSerializer.extract_and_upcreate_author(author_id=self.context["object_id"])

        # Perform the data validation.
        if not actor:
            raise serializers.ValidationError({
                'score': 'This field is required.'
            })
        if not object:
            raise serializers.ValidationError({
                'player_name': 'This field is required.'
            })

        # Return the validated values. This will be available as
        # the .validated_data property.
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








