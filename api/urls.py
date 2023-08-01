from django.urls import path
from . import views
urlpatterns = [
    path('' , views.getUser ,name='UserList'),
    path('create-user/' , views.createUser , name='create-user'),
    path('login-user/', views.loginUser , name='login-user'),
    path('create-post/' , views.createPost , name="create-post"),
    path('post-list/', views.postList , name="post-list"),
    path('like-post/' , views.likepost ,name='like-post'),
    path('comment-post/' , views.commentpost , name="comment-post"),
    path('follow/' , views.followuser , name='follow'),
    path('sendmessage/' , views.sendmsg , name='sendmessage'),
    path('getmessage/' , views.getmessages , name="getmessage"),
    path('updateprofile/' , views.updateProfile ,name='updateprofile'),
    path('requestuser-list/' , views.getrequestuser , name='request-users'),
    path('post-request-user/' , views.postrequestuser , name='post-requestUser'),
    path('create-msgroom/' , views.returnresponse , name='messageRoom'),
    path('explore-post/' , views.explorepost),
    path('searchuser/' , views.searchuser , name='search-user'),
    path('profile-post/' , views.profilepostapi),
    path('loadcomment/',views.getcomments),
    path('removeprofile/' , views.removeprofile),
    path('suggest/'  ,views.usersuggestion),
    
]