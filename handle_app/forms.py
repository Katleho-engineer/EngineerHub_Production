from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Room, User


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        # fields = ['avatar', 'username', 'email', 'first_name', 'last_name', 'bio']
        fields = ['avatar', 'first_name', 'last_name', 'bio']