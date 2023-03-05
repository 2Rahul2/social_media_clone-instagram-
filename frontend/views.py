from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from api.models import PostModel , Profile ,Chat , RequestUser , PostPrefer
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import Count
# Create your views here.
from itertools import chain




def channelTest(request,gname):
    context ={
        'group_name':gname
    }
    return render(request , 'frontend/chantest.html' , context)


@login_required(login_url="login-user")
def home(request):    
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    requests_users = RequestUser.objects.filter(reuestuser = request.user)

    return render(request ,'frontend/index1.html' , {'user':request.user ,'requestUser': requests_users,'profile':profile})

def signin(request):
    return render(request , 'frontend/signin.html')

def loginUser(request):
    return render(request , 'frontend/login.html')

@login_required(login_url="login-user")
def logoutuser(request):
    logout(request)
    return redirect("login-user")

@login_required()
def profile(request , name):
    user_model = User.objects.filter(username=name)
    # print(user_model)
    if user_model.exists():
        user = User.objects.get(username=name)
        profile_m = Profile.objects.filter(user=user)[0]

        followingobj = profile_m.myfollowing.all()
        followerobj = profile_m.myfollowers.all()
        # print('profileobject:  ',folobj.current_user)
        post_iter = PostModel.objects.filter(user=user)
        # posts = PostModel.objects.get(user=user)
        context = {
            'post':post_iter,
            'user':user_model[0],
            'profile':profile_m,
            'postcount':post_iter.count(),
            'followcount':followerobj.count(),
            'followingcount':followingobj.count(),
            
            # 'commentpost':posts.commentM.all()
        }
        return render(request , 'frontend/profile.html' ,context)
    else:
        return render(request , 'frontend/invalidprofile.html')


def editProfile(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    context = {
        'profile':profile
    }
    return render(request , 'frontend/editprofile.html',context)
def messagePage(request):
    user = User.objects.get(username = request.user)
    profile = Profile.objects.get(user = user)
    print(profile.msgid)
    # if Chat.objects.filter()
    chatobj = Chat.objects.filter(msgRoomid__in = profile.msgid)
    # print(chatobj.)

    return render(request ,'frontend/message.html' ,{'chatobj':chatobj,'user':user.username})


def explorepage(request):
    user = User.objects.get(username=request.user)
    user_profile_model = Profile.objects.get(user=user)
    # user_tags = user_profile_model.mytags.all()
    user_tags = user_profile_model.mytags.all().order_by('-weight')
    # high_tag = user_tags.annotate(count = Count('weight')).order_by('-count')
    # high_tag = PostPrefer.objects.annotate(count = Count('weight')).order_by('-count')
    # high_tag = PostPrefer.objects.all().order_by('-weight')
    print("USER TAGS:  " ,user_tags)
    lst = []
    for i in user_tags.values():
        # for j in i['postTags']:
        lst.append(i['postTags'])
    print("LIST TAGS: " ,lst)
    if lst:
        post_model = PostModel.objects.filter(tags__overlap = lst[0])[:10]
        try:
            post_model2 = PostModel.objects.filter(tags__overlap=lst[1])[:10]
            try:
                post_model3 = PostModel.objects.filter(tags__overlap = lst[2])[:10]
                try:
                    post_model4 = PostModel.objects.filter(tags__overlap = lst[3])[:10]
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
        
        # post_model1 = PostModel.objects.filter(tags__overlap = lst[2])[:1]
        pm = list(chain(post_model , post_model2 , post_model3 ,post_model4))
        print("PM: ",pm)
        for i in pm:
            print("POST MODEL:  " , i.caption)
    # post_model = PostModel.objects.filter(user__id__in = user_to_show)

    # postprefer = PostPrefer.objects.create(weight = 4)
    # postprefer.postTags.append("nature")
    # postprefer.save()
    # print("TAGS:" ,user_tags)
    return render(request , 'frontend/explore.html')

def chatpage(request,pk):
    chatobj =Chat.objects.get(msgRoomid = pk)
    user1 = User.objects.get(username = chatobj.useridOne)
    user2 = User.objects.get(username = chatobj.useridtwo)
    # print(chatobj.msg)
    # msgobj = chatobj.msg.all()[:1]
    # msgobj = Chat.objects.get(msgRoomid = pk)
    # print("message OBJECT: ",msgobj)
    # print(user1.username , user2.username ,request.user)
    if str(user1) == str(request.user):
        currentuser = user1.username
        senduser = user2.username
        senduser = Profile.objects.get(user=user2)
    elif str(user2) == str(request.user):
        currentuser = user2.username
        senduser = user1.username
        senduser = Profile.objects.get(user=user1)
    else:
        return render(request , 'frontend/invalidtextingpage.html')
    context = {
        'currentUser':currentuser,
        'senderUser':senduser,
        'chatid':pk,
    }
    return render(request , 'frontend/textingpage.html' , context)