from functools import partial
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login , logout
from rest_framework.decorators import parser_classes
from .models import Profile ,PostModel , LikeModel , CommentModel , FollowerCount ,Chat , MessagesUser , FollowerUser ,FollowingUser , RequestUser
from rest_framework.parsers import MultiPartParser
import json
from uuid import UUID
from django.core import serializers as core_serializers
from itertools import chain
import random

# Create your views here.
@api_view(['GET'])
def getUser(request):
    users = User.objects.all()
    userserializer = UserSerializer(users , many =True)
    return  Response(userserializer.data)

@api_view(['POST'])
def createUser(request):
    if request.method == 'POST':
        # print(request.data)
        data = request.data
        user_exists = User.objects.filter(username = data['username']).exists()
        if(user_exists == False):
            user = User.objects.create_user(
                username = data['username'],
                password = data['Password'],
            )
            user.save()
            user_model = User.objects.get(username=data['username'])
            profile_model = Profile.objects.create(user = user_model, id_user=user_model.id)
  
            profile_model.save()
            user_profile = ProfileSerializer(profile_model)
            return HttpResponseRedirect(redirect_to='/loginuser/')
        else:
            print('user exists')
        print(request.data)
    return Response(user_profile.data)

@api_view(['POST','GET'])
def updateProfile(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    checkUser =  User.objects.all()
    postusername = request.data['username']
    if checkUser.filter(username=postusername).exclude(username =request.user).exists():
        return Response('username taken')
    else:
        print(request.data)
    # userserializer = UserSerializer(user , data=request.data ,partial=True)
        profileserializer = ProfileSerializer(profile , data=request.data,partial=True)
        if profileserializer.is_valid():
            # userserializer.save()
            user.username = request.data['username']
            user.save()
            profileserializer.save()
            return Response({'status':'success'})
        else:
            return Response({'status':'failed'})

@api_view(['POST'])
def removeprofile(request):
    user = User.objects.get(username = request.user)
    profile = Profile.objects.get(user=user)
    # f = open('media/default.jpg' ,'r')
    # print(f)
    profile.profileimage = 'default.jpg'
    profile.save()    
    return Response("remove image")

@api_view(['POST'])
@parser_classes([MultiPartParser])
def createPost(request):
    print("hellowww")
    # post_model = PostModel.objects.all()
    username = request.data['userN']
    user = User.objects.get(username = username)
    profile_model = Profile.objects.get(user=user)
    print(request.user)


    # print(user.username)
    if request.method == "POST":
        print("user model: " , user)
        caption = request.data['caption']
        post_data = {
            'user': user,
            'postimg':request.FILES.get('postimg'),
            'caption':caption,
            'like_count':0,
            'comment_count':0,
            'profileimg':profile_model,
        }
            
        # print(request.data['postimg'])
        post_model = PostModel.objects.create(**post_data)
        post_model.save()
        get_postID = post_model.id
        get_model = PostModel.objects.get(id=get_postID)

        for i in str(caption).split("#"):
            print(i)
            get_model.tags.append(i)
        get_model.save()
        # serializer = PostModelSerializer(data=post_data)
        # if serializer.is_valid():
            # serializer.save()
            # print(serializer.data)
    return Response("data came")
    
@api_view(['POST'])
def likepost(request):
    if request.method == "POST":
        print(request.data)
        postid = request.data['post_id']
        get_postmodel_row = PostModel.objects.get(id=postid)
        if LikeModel.objects.filter(**request.data).exists():
            # print("exist already")
            get_like_model = LikeModel.objects.get(**request.data)
            # print("model:" , get_like_model)
            get_postmodel_row.likeM.remove(get_like_model)
            get_postmodel_row.like_count -= 1
            get_postmodel_row.save()
            get_like_model.delete()
        else:
            post_tags =get_postmodel_row.tags
            print(post_tags)
            print("POST TAGS:   " ,post_tags)
            user = User.objects.get(username=request.data['like_user'])
            profile = Profile.objects.get(user=user)
            serializer = LikeModelSerializer(data=request.data , context = profile)
            # profile = Profile.objects.get(user=user)

            # for tag in post_tags:
            if post_tags is not None:
                if PostPrefer.objects.filter(user=user).filter(postTags__overlap = post_tags).exists():
                    post_prefer_model = PostPrefer.objects.filter(user=user).filter(postTags__overlap =post_tags)[0]
                    post_prefer_model.weight += 1
                    post_prefer_model.save()

                    print("INCREMENT WEIGHT")
                else:
                    post_prefer = PostPrefer.objects.create(user=user , weight= 0)
                    for i in post_tags:
                        post_prefer.postTags.append(i)
                    post_prefer.save()
                    profile.mytags.add(post_prefer)
                    profile.save()
                    print("NEED TO ADD IN PREFERNCES")


            # profileImg = profile.values('profileimg')
            # print("profile in like: " , profile['profileimage'])
            if serializer.is_valid():
                serializer.save()
                obj = LikeModel.objects.get(**request.data)
                obj.profileimg = profile.profileimage
                obj.save()
                get_postmodel_row.likeM.add(obj)
                get_postmodel_row.like_count += 1
                get_postmodel_row.save()
    return Response("ohoho")



@api_view(['GET'])
def getrequestuser(request):
    user_model = User.objects.get(username=request.user)
    request_model = RequestUser.objects.filter(fromuser = user_model)
    requestserializer = RequestUserSerilaizers(request_model , many=True)
    return Response(requestserializer.data)

@api_view(['POST'])
def postrequestuser(request):
    if request.method == 'POST':
        reuest_model = User.objects.get(username=request.data['fromuser'])
        fromuser_model = User.objects.get(username=request.data['touser'])
        get_model = RequestUser.objects.get(reuestuser=reuest_model , fromuser = fromuser_model)
        if request.data['status'] == 'rejected':
            print("delete request object")
            get_model.delete()
            print(get_model)
        else:
            fromuserModel = User.objects.get(username=request.data['fromuser'])
            touserModel = User.objects.get(username=request.data['touser'])
            profilefollowing = Profile.objects.get(user=touserModel)
            profilefollower = Profile.objects.get(user=fromuserModel)
            followinguser = FollowingUser.objects.create(fromuser=fromuserModel , touser=touserModel)
            followeruser = FollowerUser.objects.create(fromuser = fromuserModel , touser=touserModel)
            # followinguser = FollowingUser(fromuser=fromuserModel , touser=touserModel)
            FollowingModel = FollowingUser.objects.get(id=followinguser.id)
            FollowerModel = FollowerUser.objects.get(id=followeruser.id)

            # FollowerModel = FollowerUser.objects
            profilefollowing.myfollowing.add(FollowingModel)
            profilefollowing.myfollowers.add(FollowerModel)

            requestFollowerObject = FollowerUser.objects.create(fromuser=touserModel , touser=fromuserModel)
            reqeustFollowingObject = FollowingUser.objects.create(fromuser=touserModel , touser=fromuserModel)
            requestFollowerModel = FollowerUser.objects.get(id=requestFollowerObject.id)
            requestFollowingModel = FollowingUser.objects.get(id=reqeustFollowingObject.id)
            profilefollower.myfollowing.add(requestFollowingModel)
            profilefollower.myfollowers.add(requestFollowerModel)

            followinguser.save()
            followeruser.save()
            profilefollowing.save()
            requestFollowerObject.save()
            reqeustFollowingObject.save()
            profilefollower.save()
            get_model.delete()
            # profilefollower.save()

            print(request.data)
        # print(request.data)
    return Response('post request user')

@api_view(['POST'])
def followuser(request):
    fromuser = User.objects.get(username=request.data['fromuser'])
    touser = User.objects.get(username=request.data['touser'])

    profilemodelfollower = Profile.objects.get(user = touser)
    profilemodelfollowing = Profile.objects.get(user = fromuser)

    if request.method == "POST":
        # if FollowerCount.objects.filter(**request.data).exists():
        #     print("already exist")
        #     followerModel = FollowerCount.objects.get(**request.data)
        #     profilemodelfollower.myfollowers.remove(followerModel)
        #     profilemodelfollower.save()
        #     profilemodelfollowing.myfollowing.remove(followerModel)
        #     profilemodelfollowing.save()
        #     followerModel.delete()
        # else:
        if FollowerUser.objects.filter(fromuser=fromuser , touser=touser).exists():
            print("alreadt exists")

            followobject = FollowerUser.objects.get(fromuser=fromuser , touser=touser)
            followingObject = FollowingUser.objects.get(fromuser=touser , touser=fromuser)
            profilemodelfollower.myfollowers.remove(followobject)
            profilemodelfollowing.myfollowing.remove(followingObject)
            profilemodelfollowing.save()
            profilemodelfollower.save()
            followobject.delete()
            followingObject.delete()
        else:
            # new stufff
            if profilemodelfollower.privateStatus == True:
                print("Request sent")
                request_model = RequestUser.objects.create(reuestuser = fromuser , fromuser = touser)
                profilemodelfollower.myrequestsuser.add(request_model)
                request_model.save()
                profilemodelfollower.save()
                # followingobj = FollowingUser.objects.create(fromuser=touser , touser=fromuser)
                # _id = followingobj.id
                # get_following = FollowingUser.objects.get(id=_id)
                # followingobj.save()
                # profilemodelfollowing.myfollowing.add(get_following)
                # profilemodelfollowing.save()
            else:
                # followSerializer = FollowUserSerializer(data=request.data)
                followeruser = FollowerUser.objects.create(fromuser = fromuser ,touser =touser)
                followinguser = FollowingUser.objects.create(fromuser = touser , touser = fromuser)
                # if followSerializer.is_valid():
                    # followSerializer.save()
                followeruser.save()
                followinguser.save()
                id1 = followeruser.id
                id2 = followinguser.id
                print("idddssssss::     " ,id1 ,id2)
                follower = FollowerUser.objects.get(id=id1)
                following = FollowingUser.objects.get(id=id2)
                profilemodelfollowing.myfollowing.add(following)
                profilemodelfollowing.save()
                profilemodelfollower.myfollowers.add(follower)
                profilemodelfollower.save()

            #old stufffs
            # print(request.data)
            # followserializer = FollowerSerializer(data=request.data)
            # if followserializer.is_valid():
            #     followserializer.save()
            #     if Chat.objects.filter(useridOne = user1.username , useridtwo = user2.username).exists() or Chat.objects.filter(useridOne = user2.username , useridtwo = user1.username).exists():
            #         print('none')
            #     else:
            #         chatRoom = Chat.objects.create(useridOne = user1.username , useridtwo =user2.username)
            #         profilemodelfollower.msgid.append(chatRoom.msgRoomid)
            #         profilemodelfollowing.msgid.append(chatRoom.msgRoomid)
            #         chatRoom.save()
            #     followerModel = FollowerCount.objects.get(**request.data)
            #     profilemodelfollower.myfollowers.add(followerModel)
            #     profilemodelfollower.save()
            #     profilemodelfollowing.myfollowing.add(followerModel)
            #     profilemodelfollowing.save()



    # serializer = FollowSerializer(followModel)
    return Response('follow datas')
@api_view(['POST' ,'GET'])
def returnresponse(request):
    if request.method == "POST":
        print(request.data)
        user1 = User.objects.get(username=request.data['fromuser'])
        user2 = User.objects.get(username=request.data['touser'])
        if Chat.objects.filter(useridOne = user1 , useridtwo = user2).exists():
            chatO = Chat.objects.get(useridOne = user1 , useridtwo =user2)            
            return Response(chatO.msgRoomid)
        if Chat.objects.filter(useridOne = user2 , useridtwo = user1).exists():
            chatO = Chat.objects.get(useridOne = user2 ,useridtwo = user1)
            return Response(chatO.msgRoomid)
        profile1 = Profile.objects.get(user=user1)
        profile2 = Profile.objects.get(user=user2)
        user_dict = {
            'useridOne':user1,'useridtwo':user2
        }
        # chatserializer = ChatSerializer(data=json.dumps(user_dict))
        chatobj = Chat.objects.create(useridOne=user1 , useridtwo=user2)
        # if chatserializer.is_valid():
        # chatserializer.save()
        chatobj.save()
        profile1.msgid.append(chatobj.msgRoomid)
        profile2.msgid.append(chatobj.msgRoomid)
        profile1.save()
        profile2.save()
        return Response(chatobj.msgRoomid)
        # else:
            # return Response('failed')
    else:
        return Response("messages")
@api_view(['POST','GET'])
def sendmsg(request):
    if request.method == "POST":
        print(request.data)
        chatObj = Chat.objects.get(msgRoomid = request.data['chatid'])
        # msgserializer = MessgaeSerializer(data=request.data)
        data = request.data
        msg_value = {
            'senderuser':User.objects.get(username =data['senderuser']),
            'recieveuser':User.objects.get(username = data['recieveuser']),
            'textmessage':data['textmessage'],
            
        }
        msg_obj = MessagesUser.objects.create(**msg_value)
        msg_obj.save()
        # if msgserializer.is_valid():
            # msgserializer.save()
        id = msg_obj.id
        msgobj = MessagesUser.objects.get(id =id)

        chatObj.msg.add(msgobj)
        chatObj.save()
        # print("ID:    ",msgserializer.data['id'])


    return Response('message data in here')

@api_view(['GET','POST'])
def getmessages(request):
    if request.method == "POST":
        messageId = request.data['cid']
        chatObj = Chat.objects.get(msgRoomid =messageId)
        # msgobj = chatObj.msg.all()
        # print(chatObj)
        # msgserilaize = json.dumps(list(msgobj.values()))
        # chatObj = Chat
        print("chat object: " ,chatObj)
        chatSerializer = ChatSerializer(chatObj)
        # chatSerializer = MessgaeSerializer(msgobj)

        # chatSerializer = core_serializers.serialize(msgserilaize)
        return Response(chatSerializer.data)
    # chatObj = Chat.objects.all()
    return Response('no data')
    # return Response(chatSerializer.data)

@api_view(['POST'])
def commentpost(request):
    print(request.data)
    if 'met' in request.data.keys():
        comment_value = CommentModel.objects.get(id=request.data['id'])
        comment_value.delete()
        post_model = PostModel.objects.get(id=request.data['post_id'])
        post_model.comment_count -= 1
        post_model.save()
        return Response(request.data['post_id'])
    else:
        user = User.objects.get(username=request.data['comment_user'])
        profile_m = Profile.objects.get(user=user)
        serializer = CommentModelSerializer(data=request.data)
        pid = request.data['post_id']
        print(pid)
        if serializer.is_valid():
            serializer.save()
            post_model_data = PostModel.objects.get(id=pid)
            comment_obj = CommentModel.objects.filter(**request.data).first()
            comment_obj.profileimg = profile_m.profileimage
            comment_obj.save()
            post_model_data.commentM.add(comment_obj)
            post_model_data.comment_count += 1
            post_model_data.save()

    return Response("comment data")
@api_view(["GET" ,"POST"])
def explorepost(request):
    exclude_list = []
    user = User.objects.get(username=request.user)
    user_profile_model = Profile.objects.get(user=user)
    # user_tags = user_profile_model.mytags.all()
    user_tags = user_profile_model.mytags.all().order_by('-weight')
    # high_tag = user_tags.annotate(count = Count('weight')).order_by('-count')
    # high_tag = PostPrefer.objects.annotate(count = Count('weight')).order_by('-count')
    # high_tag = PostPrefer.objects.all().order_by('-weight')
    # print("USER TAGS:  " ,user_tags)

    def get_post_data(exclude_list):
        lst = []
        for i in user_tags.values():
            # for j in i['postTags']:
            lst.append(i['postTags'])
        # print("LIST TAGS: " ,lst)
        if lst:
            post_model = PostModel.objects.filter(tags__overlap = lst[0]).exclude(id__in =exclude_list).order_by('?')[:4]
            # random.shuffle(post_model)
            # post_model = post_model.exclude(id__in = exclude_list)
            # post_model = post_model.exclude(id__in = exclude_list)
            # print(post_model)
            
            try:
                post_model2 = PostModel.objects.filter(tags__overlap=lst[1]).exclude(id__in =exclude_list).order_by('?')[:2]
                try:
                    post_model3 = PostModel.objects.filter(tags__overlap = lst[2]).exclude(id__in =exclude_list).order_by('?')[:3]
                    try:
                        post_model4 = PostModel.objects.filter(tags__overlap = lst[3]).exclude(id__in =exclude_list).order_by('?')[:2]
                    except:
                        post_model4 = []
                        pass
                except:
                    post_model4 = []
                    post_model3 = []
                    pass
            except:
                post_model3 = []
                post_model4 = []
                post_model2 = []

            lst_of_id = []
            # post_model1 = PostModel.objects.filter(tags__overlap = lst[2])[:1]
            pm = list(chain(post_model , post_model2 , post_model3 ,post_model4))
            # print("PM: ",pm)
            for i in pm:
                lst_of_id.append(i.id)
            
            # print("POST MODEL:  " , lst_of_id)
            random.shuffle(pm)
            postserilaize = PostModelSerializer(pm , many=True)

        return postserilaize.data

    if request.method == "POST":
        print("POST DATA   :    ",request.data)
        exclude_list = request.data['post_id']
        return Response(get_post_data(exclude_list))
    else:
    # get_post_data(exclude_list)
        return Response(get_post_data(exclude_list))

@api_view(['POST'])
def searchuser(request):
    if request.method == "POST":
        print(request.data)
        # lst = [request.data['value']]
        profile_model = Profile.objects.filter(user__username__icontains = request.data['value'])
        print(profile_model)
        profile_serializer = SearchProfileSerilaizer(profile_model , many=True)

        # return JsonResponse(json.dumps(profile_model.values))
    return Response(profile_serializer.data)

@api_view(['GET'])
def postList(request):
    user_model = User.objects.get(username=request.user)
    print("user_model:     " , user_model)
    profile = Profile.objects.get(user=user_model)
    profile_follower = profile.myfollowing.filter(touser=user_model)
    f = profile_follower.all()
    lst_user = f.values_list('fromuser_id' ,flat=True)
    user_to_show = User.objects.filter(id__in =lst_user)
    print(user_to_show.values_list('username' ,flat=True))
    # post_model = PostModel.objects.filter(user__fwfromuser = )
    # current user posts too
    post_model = PostModel.objects.filter(user__id__in = user_to_show).order_by('-datecreated')
    # print(post_model)
    postserializer = PostModelSerializer(post_model , many=True)
    return Response(postserializer.data)

    # return Response(serializer.data)

@api_view(['POST'])
def getcomments(request):
    if request.method == "POST":
        pID = request.data['post_id']
        fi = request.data['prev_index']
        si = request.data['last_index']
        comments = CommentModel.objects.filter(post_id = pID)[fi:si]
        print("INDEX VALUES:     " , fi ,si)
        comment_serilaizer = CommentModelSerializer(comments , many=True)
        return Response(comment_serilaizer.data)
    return Response('trial')
@api_view(['POST'])
def loginUser(request):
    if request.method == "POST":
        data = request.data
        user = authenticate(request , username=data['username'] , password = data['Password'])
        if user is not None:
            login(request , user)
        print(request.data)
    return Response("data came")
    

@api_view(['GET' , 'POST'])
def profilepostapi(request):
    if request.method == 'POST':
        user = User.objects.get(username =request.data['name'])
        profile_post = PostModel.objects.filter(user=user)

        post_serilaizer = PostModelEverySerilaizer(profile_post , many=True)
        return Response(post_serilaizer.data)
    return Response('No data')

@api_view(['GET'])
def usersuggestion(request):
    # print("suggestion method: " ,request.user)
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    myfollow = profile.myfollowing
    lst = []
    print("myfollow list:     " ,myfollow.values())
    for i in myfollow.values():
        lst.append(i['fromuser_id'])
    print("list value are:    " ,lst)
    follower_profile = Profile.objects.filter(user__id__in = lst)
    for i in follower_profile:
        for j in i.myfollowing.values():
            print("loop value:  " ,j)
    # follower_profile_following_list = follower_profile.myfollowing
    # follow_users = myfollow.touser
    profileserilaizer = SuggestProfileSerilaizer(follower_profile , many=True)
    # print("hehehheheheheh",follower_profile_following_list.all())
    return Response(profileserilaizer.data)



    