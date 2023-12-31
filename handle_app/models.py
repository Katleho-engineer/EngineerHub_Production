from django.db import models

from django.contrib.auth.models import User, AbstractUser
# from django.contrib.auth.models import User


class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=250, null=True, blank=True)
    avatar = models.ImageField(null=True, default='avatar.svg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


'''
class Profile(models.Model):
    bio = models.TextField(max_length=250, null=True, blank=True)
    avatar = models.ImageField(null=True, default='avatar.svg')
'''


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='host_rooms')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, related_name='room_topic')
    name = models.CharField(max_length=140)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host_messages')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='room_messages')
    body = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:40]
