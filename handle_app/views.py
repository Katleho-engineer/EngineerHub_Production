from django.shortcuts import render, redirect

from django.db.models import Q

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Room, Topic, Message, User

from .forms import RoomForm, MyUserCreationForm, UserForm

# Create your views here.


def roomsPage(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    rooms = Room.objects.filter(
        Q(topic__name__contains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    room_count = rooms.count()

    current_user = request.user.username
    user_info = User.objects.get(username=current_user)

    p = Paginator(rooms, 2)
    page_number = request.GET.get('page')

    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    context = {
        'page_obj': page_obj,
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,
        'user_info': user_info,
    }
    return render(request, 'handle/rooms.html', context)


def TestPage(request, pk):
    room = Room.objects.get(pk=pk)
    # message = Message.objects.all().user
    output = room.room_messages.all()
    context = {
        'room': room,
        'messages': output
    }

    return render(request, 'handle/test.html', context)


def roomDetailPage(request, pk):
    room = Room.objects.get(pk=pk)
    room_messages = room.room_messages.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room-detail', pk=room.id)

    all_rooms = Room.objects.all()

    current_user = request.user.username
    user_info = User.objects.get(username=current_user)

    context = {
        'all_rooms': all_rooms,
        'room': room,
        'messages': room_messages,
        'participants': participants,
        'user_info': user_info,
    }
    return render(request, 'handle/room_detail.html', context)


def createRoomPage(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('rooms')

    current_user = request.user.username
    user_info = User.objects.get(username=current_user)

    context = {
        'form': form,
        'user_info': user_info,
    }
    return render(request, 'handle/create_room.html', context)


def updateRoomPage(request, pk):
    room = Room.objects.get(pk=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('rooms')

    current_user = request.user.username
    user_info = User.objects.get(username=current_user)

    context = {
        'form': form,
        'user_info': user_info,
    }
    return render(request, 'handle/create_room.html', context)


def deleteRoomPage(request, pk):
    room = Room.objects.get(pk=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('rooms')

    context = {
        'obj': room,
        'name': 'room-d'
    }
    return render(request, 'handle/delete.html', context)


def deleteMessagePage(request, pk):
    message = Message.objects.get(pk=pk)

    if request.method == 'POST':
        message.delete()
        return redirect('rooms')

    context = {
        'obj': message,
    }
    return render(request, 'handle/delete.html', context)


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('rooms')

        else:
            messages.error(request, 'An error occurred during registrations.')

    context = {
        'form': form,
    }
    return render(request, 'handle/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('rooms')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('rooms')
        else:
            messages.error(request, 'Email or Password does not exist.')

    return render(request, 'handle/login.html')


def logoutPage(request):
    logout(request)
    return redirect('login')


def userProfilePage(request, pk):
    user = User.objects.get(id=pk)

    rooms = user.host_rooms.all()
    room_messages = user.host_messages.all()
    topics = Topic.objects.all()

    current_user = request.user.username
    user_info = User.objects.get(username=current_user)

    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,
        'user_info': user_info,
    }

    return render(request, 'handle/profile.html', context)


def updateUserPage(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
        else:
            context = {
                'form': form,
                'email': user.email,
                'username': user.username
            }
            return render(request, 'handle/test.html', context)

    context = {
        'form': form,
    }
    return render(request, 'handle/update_user.html', context)