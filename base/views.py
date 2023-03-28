from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
# Create your views here.


def LoginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'O usuário não existe!')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuário e/ou Senha não estão corretos!')

    context = {'page': page}
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(
                request, 'Um erro aconteceu durante o processo de registro!')

    context = {'form': form}
    return render(request, 'login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    rooms_count = rooms.count()
    rooms_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[:5]
    topics = Topic.objects.annotate(
        num_rooms=Count('room')).order_by('-num_rooms', 'name')[:5]
    context = {'rooms': rooms, 'topics': topics,
               'rooms_count': rooms_count, 'rooms_messages': rooms_messages}
    return render(request, 'home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST' and request.user.is_authenticated:
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    rooms_messages = user.message_set.all()[:15]
    topics = Topic.objects.annotate(
        num_rooms=Count('room')).order_by('-num_rooms', 'name')[:5]
    context = {'user': user, 'rooms': rooms,
               'rooms_messages': rooms_messages, 'topics': topics}
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def updateProfile(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {'form': form}
    return render(request, 'update-profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all().order_by('name')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room = Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        room.participants.add(request.user)
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all().order_by('name')
    if request.user != room.host and not request.user.is_staff:
        return HttpResponse('Você não tem permissão para isso!')
    form = RoomForm(instance=room)
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form, 'room': room, 'topics': topics}
    return render(request, 'room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host and not request.user.is_staff:
        return HttpResponse('Você não tem permissão para isso!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'delete.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    delete_message = Message.objects.get(id=pk)
    room = delete_message.room
    user_room_messages_count = Message.objects.filter(
        Q(room=room) & Q(user=request.user)).count()
    if request.user != delete_message.user and not request.user.is_staff:
        return HttpResponse('Você não tem permissão para isso!')
    if request.method == 'POST':
        delete_message.delete()
        if user_room_messages_count == 1 and request.user != room.host:
            room.participants.remove(request.user)
        return redirect('home')
    context = {'obj': delete_message}
    return render(request, 'delete.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    if q != '':
        topics = Topic.objects.filter(
            Q(name__icontains=q)
        ).annotate(num_rooms=Count('room')).order_by('-num_rooms', 'name')
    else:
        topics = Topic.objects.filter(
            Q(name__icontains=q)
        ).order_by('name')
    context = {'topics': topics}
    return render(request, 'topics.html', context)


def activityPage(request):
    rooms_messages = Message.objects.all()[:15]
    context = {'rooms_messages': rooms_messages}
    return render(request, 'activity.html', context)
