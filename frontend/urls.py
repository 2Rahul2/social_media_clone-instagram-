from django import views
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home ,name='home'),
    path('signin/' , views.signin , name='signin'),
    path('loginuser/', views.loginUser , name="login-user"),
    path('logout' ,views.logoutuser , name="logout-user"),
    path('profile/<str:name>' , views.profile , name='profile'),
    path('text/<str:pk>/' , views.chatpage , name="chat-page"),
    path('message/' , views.messagePage , name='msgpage'),
    path('edit' ,views.editProfile , name="edit-profile"),
    path('chan/<str:gname>/' , views.channelTest , name='cTest'),
    path('explore/' , views.explorepage),
    
]