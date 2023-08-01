from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from django.contrib.auth.models import User 
from .models import *


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowerCount
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username' ,'email',]
        # read_only_fields = ('id' , 'username')


class RequestUserSerilaizers(serializers.ModelSerializer):
    reuestuser = UserSerializer()
    fromuser = UserSerializer()
    class Meta:
        model = RequestUser
        fields = '__all__'

class FollowUserSerializer(serializers.ModelSerializer):
    fromuser = UserSerializer()
    touser = UserSerializer()

    class Meta:
        model = FollowerUser
        fields = ['fromuser' ,'touser' ,'id']

class MessgaeSerializer(serializers.ModelSerializer):
    senderuser = UserSerializer()
    recieveuser = UserSerializer()
    class Meta:
        model = MessagesUser
        fields = ['senderuser' ,'recieveuser' ,'textmessage' ,'id' ,'createdat']

class ChatSerializer(serializers.ModelSerializer):
    useridOne = UserSerializer()
    useridtwo = UserSerializer()
    msg = MessgaeSerializer(many=True)
    class Meta:
        model = Chat
        fields = '__all__'
        depth = 1


class ProfileSerializer(serializers.ModelSerializer):
    myfollowers = FollowerSerializer(many=True)
    myfollowing = FollowerSerializer(many=True)
    class Meta:
        model = Profile
        fields = '__all__'
class SuggestProfileSerilaizer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['user' ,'profileimage']

class LikeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeModel
        fields = ['post_id' ,'like_user' ,'profileimg']


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['id' ,'post_id' , 'comment' , 'comment_user' ,'profileimg']

class ProfilePostmodelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profileimage']

class PostModelSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # likeM = LikeModelSerializer(many=True)
    # commentM = CommentModelSerializer(many=True)
    profileimg = ProfilePostmodelSerializer()
    # postimg = serializers.ImageField(use_url =True)
    class Meta:
        model = PostModel
        fields = ['id','user','postimg','caption' ,'like_count','comment_count','datecreated','profileimg']
        depth = 2

class PostModelEverySerilaizer(serializers.ModelSerializer):
    user = UserSerializer()
    likeM = LikeModelSerializer()
    commentM = CommentModelSerializer()
    profileimg = ProfilePostmodelSerializer()
    postimg = serializers.ImageField(use_url =True)

    class Meta:
        model=PostModel
        fields='__all__'
        depth = 2

class SearchProfileSerilaizer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['user']