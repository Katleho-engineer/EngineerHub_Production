from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import status

from rest_framework.authtoken.models import Token
from . import models

from handle_app.models import Room, Message, User, Topic
from .serializers import RoomSerializer, MessageSerializer, TopicSerializer, RegistrationSerializer, CreateRoomSerializer


class RoomsPage(ListAPIView):
    """
        get:
        Return a list of all the existing rooms.

        post:
        Create a new room instance.
     """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomsPage(CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Room.objects.all()
    serializer_class = CreateRoomSerializer


class RoomDetailPage(RetrieveUpdateDestroyAPIView):
    """
        get:
        Return a particular room.

        put:
        Update a particular room.

        patch:
        Update a particular section of the room.

        delete:
        Delete a particular room.
    """
    permission_classes = [IsAuthenticated]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class MessagesPage(ListAPIView):
    """
        get:
        Return a list of all the existing messages.

     """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class RoomMessages(ListCreateAPIView):
    """
        get:
        Return a list of all the existing room messages.

        post:
        Create a message in a particular room.
     """
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Message.objects.filter(room_id=pk)


class UserMessages(ListCreateAPIView):
    """
        get:
        Return a list of all the existing user messages.

        post:
        Create a message in a particular room for a specific user.
     """
    serializer_class = MessageSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Message.objects.filter(user_id=pk)


class Topics(ListCreateAPIView):
    """
        get:
        Return a list of all the existing topics.

        post:
        Create a topic instance.
     """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAdminUser]


class Topic(RetrieveUpdateDestroyAPIView):
    """
        get:
        Return a particular topic.

        put:
        Update a particular topic.

        delete:
        Delete a particular topic.
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAdminUser]


@api_view(['POST'])
def Registration(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['response'] = 'Registration Successful'
            data['username'] = account.username
            data['email'] = account.email

            token = Token.objects.get(user=account).key

            data['token'] = token

        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def Logout(request):

    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)