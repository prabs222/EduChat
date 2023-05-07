from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.add_message(request, messages.INFO, "User does not exist")
        user = authenticate(request, username = username, password = password)    
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,  "Invalid credentials")
            
    context = {"page": page}
    return render(request,'login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()    
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,  "An error occurred while registration")

            
    context = {"form":form}
    return render(request,'login_register.html',context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q) 
                                )
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    topics = Topic.objects.all()
    context = {"rooms": rooms, "topics": topics,"room_count": room_count, "room_messages": room_messages}
    return render(request,'home.html',context)


@login_required(login_url='login/')
def createRoom(request):
    form = RoomForm
    context = {'form': form}
    if request.method == 'POST':
        form = RoomForm(request.POST)    
        if form.is_valid:
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')

    return render(request,'createRoom.html',context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    context = {"user": user, "topics": topics, "rooms": rooms, "room_messages": room_messages}
    return render(request,'userProfile.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST' and request.user.is_authenticated:
        addMessage = request.POST.get('message')
        user = User.objects.get(username = request.user)
        Message.objects.create(message = addMessage, room=room, user = user)
        room.participants.add(request.user)
        messages.success(request,  "message added successfully")
        return redirect('room',pk)
    
    context = {"room": room, "room_messages": room_messages, "participants": participants}
    return render(request,'room.html',context)

@login_required(login_url='login/')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    context = {"form": form}
    if request.user != room.host:
        return HttpResponse("You are not allowed to edit this room")
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)    
        if form.is_valid:
            newRoom = form.save()
            return redirect('home')
    return render(request,'updateRoom.html',context)

@login_required(login_url='login/')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    context = {'obj':room}
    
    if request.user != room.host:
        return HttpResponse("You are not allowed to delete this room")
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
        
    return render(request, 'delete.html', context)
    
@login_required(login_url='login/')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    context = {'obj':message}
    
    if request.user != message.user:
        return HttpResponse("You are not allowed to delete this room")
    
    if request.method == 'POST':
        message.delete()
        return redirect('room',message.room.id)
        
    return render(request, 'delete.html', context)
    