from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from handle_app.models import Room, Topic, Message, User


class RegistrationSerializer(ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password2': {'write_only': True},
        }

    def save(self, **kwargs):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error': 'P1 and P2 should be the same.'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exist.'})

        if User.objects.filter(username=self.validated_data['username']).exists():
            raise serializers.ValidationError({'error': 'Username already exist.'})

        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()

        return account


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class CreateRoomSerializer(ModelSerializer):
    topic = TopicSerializer(read_only=True)
    host = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Room
        fields = ['host', 'topic', 'name', 'description']
        extra_kwargs = {
            'host': {'read_only': True},
        }


class RoomSerializer(ModelSerializer):
    '''
    # Create a custom method field
    host = serializers.SerializerMethodField('_user')

    # Use this method for the custom field
    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user
    '''

    host = UserSerializer(read_only=True)
    topic = TopicSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ['host', 'topic', 'name', 'description', 'created', 'updated']
        # exclude = ['participants']


class MessageSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    # room = RoomSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        # fields = ['room', 'body']


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'
