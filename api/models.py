from email.policy import default
from pyexpat import model
from uuid import uuid4
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()
class FollowerCount(models.Model):
    user_follower = models.CharField(max_length=100 , null=True ,blank=True)
    current_user = models.CharField(max_length=100 , null=True ,blank=True)

    def __str__(self):
        return self.user_follower
    

class MessagesUser(models.Model):
    senderuser = models.ForeignKey(User , on_delete=models.SET_NULL , blank=True , null=True)
    recieveuser = models.ForeignKey(User ,on_delete=models.SET_NULL , blank=True , null=True , related_name="recUser")
    createdat = models.DateTimeField(auto_now_add=True , blank=True)
    textmessage = models.CharField(max_length=700)
    
    class Meta:
        ordering = ['id']

class Chat(models.Model):
    msgRoomid = models.UUIDField(default=uuid.uuid4 , editable=False , primary_key=True)
    msg = models.ManyToManyField(MessagesUser , blank=True)
    useridOne = models.ForeignKey(User , on_delete=models.SET_NULL , blank=True ,null=True , related_name='oneUser')
    useridtwo = models.ForeignKey(User,blank=True , on_delete=models.SET_NULL , null=True)

class FollowerUser(models.Model):
    fromuser = models.ForeignKey(User , on_delete=models.SET_NULL ,null=True , blank=True ,related_name='fufromuser')
    touser = models.ForeignKey(User , on_delete=models.SET_NULL, blank=True ,null=True ,related_name='futouser')

    def __str__(self):
        return self.touser.username
class FollowingUser(models.Model):
    fromuser = models.ForeignKey(User , on_delete=models.SET_NULL ,null=True, blank=True ,related_name='fwfromuser')
    touser = models.ForeignKey(User , on_delete=models.SET_NULL,null=True, blank=True ,related_name='fwtouser')

    def __str__(self):
        return self.fromuser.username
class RequestUser(models.Model):
    reuestuser = models.ForeignKey(User , on_delete=models.SET_NULL , null=True , blank=True , related_name='reqUser')
    fromuser = models.ForeignKey(User ,on_delete=models.SET_NULL ,blank=True ,null=True)

    def __str__(self):
        return self.fromuser.username


class PostPrefer(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , null=True , blank=True)
    postTags = ArrayField(models.CharField(max_length=80), default=list , blank=True , size=50)
    weight = models.SmallIntegerField(null=True ,blank=True)
    def __str__(self):
        return str(self.weight)

class SuggestUser(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Profile(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    id_user = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100 , blank=True)
    profileimage = models.ImageField(upload_to = "user_profile" ,default='default.jpg' , blank=True , null=True)
    privateStatus = models.BooleanField(default=False)
    name = models.CharField(max_length=50 ,null=True ,blank=True)
    myfollowers = models.ManyToManyField(FollowerUser ,blank=True , related_name='fol_use')
    myfollowing = models.ManyToManyField(FollowingUser , blank=True , related_name='mefollow')
    msgid = ArrayField(models.CharField(max_length=100) , blank=True ,default=list)
    mytags = models.ManyToManyField(PostPrefer , blank=True)    
    suggestionuser = models.ManyToManyField(SuggestUser , blank=True ,null=True)
    myrequestsuser = models.ManyToManyField(RequestUser ,blank=True)

    def __str__(self):
        return self.user.username


class LikeModel(models.Model):
    post_id = models.UUIDField(default=0)
    like_user = models.CharField(max_length=100 ,null=True)
    profileimg = models.ImageField(blank=True , null=True)

    def __str__(self):
        return self.like_user
class CommentModel(models.Model):
    post_id = models.UUIDField(default=0)
    comment = models.CharField(max_length=400 , null=True)
    comment_user = models.CharField(max_length=100 , null=True)
    profileimg = models.ImageField(blank=True , null=True)

    def __str__(self):
        return self.comment_user
class PostModel(models.Model):
    id = models.UUIDField(primary_key=True ,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    postimg = models.ImageField(upload_to = "post_images" , blank =True)
    caption = models.CharField(max_length=100)
    like_count = models.IntegerField()
    comment_count = models.IntegerField()
    datecreated = models.DateTimeField(auto_now_add=True)
    likeM = models.ManyToManyField(LikeModel  , blank=True)
    commentM = models.ManyToManyField(CommentModel ,blank=True)
    profileimg = models.ForeignKey(Profile , on_delete=models.CASCADE ,null=True , blank=True)
    
    tags = ArrayField(models.CharField(max_length=80) , blank=True  , null=True , default=list)
    def __str__(self):
        return self.user.username
    class Meta:
        ordering = ['-datecreated']


