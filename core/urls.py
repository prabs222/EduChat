from django.urls import path
# from .views import *
from .views import * 

urlpatterns = [
    path('',home,name='home'),
    path('create-room',createRoom, name='create-room'),
    path('room/<str:pk>/',room, name='room'),
    path('update-room/<str:pk>/',updateRoom, name='update-room'),
    path('delete-room/<str:pk>/',deleteRoom, name='delete-room'),
    
    path('login/',loginPage,name = 'login'),
    path('logout/',logoutPage,name = 'logout'),
    path('register/',registerPage,name = 'register'),
    path('user-profile/<str:pk>/',userProfile, name='user-profile'),
    
    path('delete-message/<str:pk>/',deleteMessage, name='delete-message'),
    
    path('updateUser/', updateUser, name='update-user'),

    path('topics/', topicsPage, name='topics'),
    path('activity/', activityPage, name='activity'),

] 
